from datetime import datetime, timedelta, timezone
from os.path import join
from tempfile import gettempdir

from pytest import raises
import responses as resp  # noqa: I201

from ssaw import ExportApi
from ssaw.exceptions import NotFoundError
from ssaw.models import ExportJob


from . import load_fixture, my_vcr


@my_vcr.use_cassette()
def test_export_notfound(session):
    with raises(NotFoundError):
        assert ExportApi(session).get_info(123)


@my_vcr.use_cassette()
def test_export_info(session):

    r = ExportApi(session).get_info(1)
    assert isinstance(r, ExportJob), 'Should get back an ExportJob object'
    assert r.job_id == 1, "Should get back the same job id"


@my_vcr.use_cassette()
def test_export_start_cancel(session, params, capsys):
    api = ExportApi(session)
    job = ExportJob(questionnaire_id=params['QuestionnaireId'], export_type="Paradata")
    r = api.start(job)
    assert isinstance(r, ExportJob), "Should get back the created job"
    r = api.cancel(r.job_id)
    assert r is None, 'Does not return anything'
    captured = capsys.readouterr()
    assert captured.out == "No running export process was found\n"

    r = api.start(job, wait=True, show_progress=True)
    captured = capsys.readouterr()
    assert captured.out == "Generating...\n..\n"


@my_vcr.use_cassette()
def test_export_get(session, params):
    tempdir = gettempdir()
    api = ExportApi(session)

    r = api.get(questionnaire_identity=params['QuestionnaireId'],
                export_path=tempdir, export_type='Tabular')
    assert r == join(tempdir, 'ssaw_1_Tabular_All.zip')

    job = next(api.get_list(questionnaire_identity=params['QuestionnaireId'], export_type='Tabular'))

    local_start_date = job.start_date.replace(tzinfo=timezone.utc)
    age = (datetime.now(timezone.utc) - local_start_date).total_seconds() / 60  # age in minutes of the last export

    r = api.get(questionnaire_identity=params['QuestionnaireId'],
                export_path=tempdir, export_type='Tabular', limit_age=int(age) - 1)
    assert r is None

    r = api.get(questionnaire_identity=params['QuestionnaireId'],
                export_path=tempdir, export_type='Tabular', limit_date=local_start_date + timedelta(seconds=10))
    assert r is None

    r = api.get(questionnaire_identity=params['QuestionnaireId'],
                export_path=tempdir, export_type='Tabular', limit_date=local_start_date - timedelta(seconds=10))
    assert r == join(tempdir, 'ssaw_1_Tabular_All.zip')

    r = api.get(questionnaire_identity=params['QuestionnaireId'],
                export_path=tempdir, export_type='SPSS')

    assert r is None

    r = api.get(questionnaire_identity=params['QuestionnaireId'],
                export_path=tempdir, export_type='Paradata', generate=True)

    assert r == join(tempdir, 'ssaw_1_Paradata_All.zip')


# ---------------------------------------------------------------------------
# responses-based tests – no live server required
# ---------------------------------------------------------------------------

_WS = "primary"
_BASE = "http://localhost:9707"
_EXPORT_URL = f"{_BASE}/{_WS}/api/v2/export"
_QID = "5a99cf9de0e24e4f9da98af998129868$1"


def _completed_fixture(job_id: int = 42) -> dict:
    """Return a fixture representing a completed export job."""
    return {
        "JobId": job_id,
        "ExportStatus": "Completed",
        "StartDate": "2026-01-01T00:00:00Z",
        "CompleteDate": "2026-01-01T00:01:00Z",
        "Progress": 100,
        "ETA": None,
        "Error": None,
        "Links": {"Cancel": None, "Download": f"http://localhost:9707/primary/api/v2/export/{job_id}/file"},
        "HasExportFile": True,
        "ExportType": "SPSS",
        "QuestionnaireId": _QID,
        "InterviewStatus": "All",
        "From": None,
        "To": None,
        "AccessToken": None,
        "RefreshToken": None,
        "StorageType": None,
        "TranslationId": None,
        "IncludeMeta": False,
    }


def test_export_job_defaults_not_serialized():
    """None defaults for storage_type, from_date, to_date etc. must be excluded from the payload."""
    job = ExportJob(questionnaire_id=_QID, export_type="SPSS", interview_status="All")
    payload = job.model_dump(mode='json', by_alias=True, exclude_none=True)
    for field in ("StorageType", "From", "To", "AccessToken", "RefreshToken"):
        assert field not in payload, f"{field} should not appear in serialized payload when not set"


def test_export_job_datetime_is_json_serializable():
    """Regression test for issue #5: from_date/to_date must serialize to strings, not datetime objects."""
    import json
    from datetime import datetime
    job = ExportJob(questionnaire_id=_QID, export_type="SPSS",
                    from_date=datetime(2024, 1, 1), to_date=datetime(2024, 12, 31))
    payload = job.model_dump(mode='json', by_alias=True, exclude_none=True)
    assert isinstance(payload["From"], str), "from_date must serialize to a string"
    assert isinstance(payload["To"], str), "to_date must serialize to a string"
    json.dumps(payload)  # must not raise TypeError


@resp.activate
def test_export_start_wait_polls_to_completion(responses_client, monkeypatch):
    """start(wait=True) keeps polling get_info until export_status is Completed."""
    import ssaw.export as exp_module
    monkeypatch.setattr(exp_module.time, "sleep", lambda _: None)

    running = load_fixture("export_job_running.json")
    completed = _completed_fixture()

    resp.add(resp.POST, _EXPORT_URL, json=running, status=200)
    resp.add(resp.GET, f"{_EXPORT_URL}/42", json=running, status=200)    # initial get_info
    resp.add(resp.GET, f"{_EXPORT_URL}/42", json=running, status=200)    # first poll
    resp.add(resp.GET, f"{_EXPORT_URL}/42", json=completed, status=200)  # second poll → done

    result = ExportApi(responses_client).start(
        ExportJob(questionnaire_id=_QID, export_type="SPSS"),
        wait=True,
    )

    assert result.export_status == "Completed"
    assert result.has_export_file is True


@resp.activate
def test_export_start_wait_exits_on_fail(responses_client, monkeypatch):
    """start(wait=True) stops polling immediately when export_status is Fail."""
    import ssaw.export as exp_module
    monkeypatch.setattr(exp_module.time, "sleep", lambda _: None)

    running = load_fixture("export_job_running.json")
    failed = {**running, "ExportStatus": "Fail"}

    resp.add(resp.POST, _EXPORT_URL, json=running, status=200)
    resp.add(resp.GET, f"{_EXPORT_URL}/42", json=running, status=200)  # initial get_info
    resp.add(resp.GET, f"{_EXPORT_URL}/42", json=failed, status=200)   # first poll → Fail

    result = ExportApi(responses_client).start(
        ExportJob(questionnaire_id=_QID, export_type="SPSS"),
        wait=True,
    )

    assert result.export_status == "Fail"


@resp.activate
def test_export_start_wait_respects_timeout(responses_client, monkeypatch):
    """start(wait=True, timeout=0) returns after only the initial get_info, without entering the poll loop."""
    import ssaw.export as exp_module
    monkeypatch.setattr(exp_module.time, "sleep", lambda _: None)

    running = load_fixture("export_job_running.json")

    resp.add(resp.POST, _EXPORT_URL, json=running, status=200)
    resp.add(resp.GET, f"{_EXPORT_URL}/42", json=running, status=200)  # initial get_info only

    result = ExportApi(responses_client).start(
        ExportJob(questionnaire_id=_QID, export_type="SPSS"),
        wait=True,
        timeout=0,
    )

    # Still running — loop never entered because elapsed(0) is not < timeout(0)
    assert result.export_status == "Running"
    assert len(resp.calls) == 2  # POST + one GET (no poll loop)


@resp.activate
def test_export_get_generate_no_prior_export(responses_client, monkeypatch, tmp_path):
    """Regression test for issue #10: get(..., generate=True) must not raise ValidationError
    when no prior export exists and a new job must be started."""
    import ssaw.export as exp_module
    monkeypatch.setattr(exp_module.time, "sleep", lambda _: None)

    running = load_fixture("export_job_running.json")
    completed = _completed_fixture()
    zip_content = b"PK fake zip content"

    # Call order inside get() → start(wait=True):
    # 1. GET list (get_list via _get_first_suitable) → empty, no prior export
    resp.add(resp.GET, _EXPORT_URL, json=[], status=200)
    # 2. POST (start) → running job created
    resp.add(resp.POST, _EXPORT_URL, json=running, status=200)
    # 3. GET /42 (initial get_info before the poll loop) → still running
    resp.add(resp.GET, f"{_EXPORT_URL}/42", json=running, status=200)
    # 4. GET /42 (first poll iteration) → completed, exits loop
    resp.add(resp.GET, f"{_EXPORT_URL}/42", json=completed, status=200)
    # 5. GET download link
    resp.add(resp.GET, "http://localhost:9707/primary/api/v2/export/42/file",
             body=zip_content,
             headers={"Content-Type": "application/zip",
                      "Content-Disposition": 'attachment; filename="export.zip"'},
             status=200)

    result = ExportApi(responses_client).get(
        questionnaire_identity=_QID,
        export_type="SPSS",
        interview_status="All",
        export_path=str(tmp_path),
        generate=True,
    )

    assert result is not None
    assert result.endswith(".zip")
