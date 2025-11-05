from datetime import datetime, timedelta, timezone
from os.path import join
from tempfile import gettempdir

from pytest import raises

from ssaw import ExportApi
from ssaw.exceptions import NotFoundError
from ssaw.models import ExportJob


from . import my_vcr


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
