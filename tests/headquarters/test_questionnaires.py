import json
import types
from os.path import join
from tempfile import gettempdir
from uuid import UUID

from pytest import fixture
import responses as resp  # noqa: I201

from ssaw import QuestionnairesApi
from ssaw.headquarters_schema import Interview, Questionnaire
from ssaw.models import CriticalityLevel

from . import load_fixture, my_vcr
from ..utils import create_assignment

_WS = "primary"


@fixture
def statuses():
    return ['RejectedBySupervisor', 'Completed', 'ApprovedBySupervisor']


@my_vcr.use_cassette()
def test_interview_statuses(session, statuses):
    """Tests an API call to get interview statuses"""

    response = QuestionnairesApi(session).statuses()

    assert isinstance(response, list)
    assert set(statuses).issubset(response), "All keys should be in the response"


@my_vcr.use_cassette()
def test_questionnaire_list(session, params):
    TOTAL_QUESTIONNAIRES = 103
    response = QuestionnairesApi(session).get_list()
    assert isinstance(response, types.GeneratorType)
    assert isinstance(next(response), Questionnaire), "Should be list of Questionnaire objects"
    assert len(list(response)) == TOTAL_QUESTIONNAIRES - 1, "We have to have all items returned"

    response = QuestionnairesApi(session).get_list(skip=5)
    assert next(response).version == 7

    response = QuestionnairesApi(session).get_list(take=5)
    assert len(list(response)) == 5

    response = QuestionnairesApi(session).get_list(questionnaire_id=params['TemplateId'],
                                                   version=params['TemplateVersion'])
    assert len(list(response)) == 1


@my_vcr.use_cassette(decode_compressed_response=True)
def test_questionnaire_document(session, params):
    response = QuestionnairesApi(session).document(params['TemplateId'], params['TemplateVersion'])
    assert response.public_key == UUID(params['TemplateId'])


@my_vcr.use_cassette()
def test_questionnaire_interviews(session, params):
    response = QuestionnairesApi(session).interviews(params['TemplateId'], params['TemplateVersion'])
    assert isinstance(response, types.GeneratorType)
    assert isinstance(next(response), Interview), "Should be list of Interview objects"


@my_vcr.use_cassette()
def test_questionnaire_recordaudio(session, params):
    response = QuestionnairesApi(session).update_recordaudio(params['TemplateId'], params['TemplateVersion'], True)
    assert response is None


@my_vcr.use_cassette()
def test_questionnaire_download_weblinks(admin_session, params):
    _ = create_assignment(admin_session, "inter1", params['QuestionnaireId'], identifying_data=[], webmode=True)
    response = QuestionnairesApi(admin_session).download_web_links(params['TemplateId'], params['TemplateVersion'])
    assert hasattr(response[0], "link")

    tempdir = gettempdir()
    response = QuestionnairesApi(admin_session).download_web_links(params['TemplateId'],
                                                                   params['TemplateVersion'], path=tempdir)
    assert response == join(tempdir, "Web ssaw package test questionnaire (ver. 1).zip")


# ---------------------------------------------------------------------------
# responses-based tests – no live server required
# ---------------------------------------------------------------------------

_Q_ID = "aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa"
_Q_VERSION = 1


@resp.activate
def test_questionnaire_get_criticality_level(responses_client):
    """get_criticality_level() returns the current level string."""
    fixture = load_fixture("criticality_level.json")
    resp.add(
        resp.GET,
        f"http://localhost:9707/{_WS}/api/v1/questionnaires/{_Q_ID}/{_Q_VERSION}/criticalityLevel",
        json=fixture,
        status=200,
    )

    result = QuestionnairesApi(responses_client).get_criticality_level(_Q_ID, _Q_VERSION)

    assert result == CriticalityLevel.WARN.value


@resp.activate
def test_questionnaire_set_criticality_level(responses_client):
    """set_criticality_level() sends the correct JSON payload."""
    resp.add(
        resp.POST,
        f"http://localhost:9707/{_WS}/api/v1/questionnaires/{_Q_ID}/{_Q_VERSION}/criticalityLevel",
        status=204,
    )

    QuestionnairesApi(responses_client).set_criticality_level(_Q_ID, _Q_VERSION, CriticalityLevel.BLOCK)

    assert len(resp.calls) == 1
    sent = json.loads(resp.calls[0].request.body)
    assert sent["CriticalityLevel"] == CriticalityLevel.BLOCK.value


@resp.activate
def test_questionnaire_set_criticality_level_str(responses_client):
    """set_criticality_level() also accepts a plain string for the level."""
    resp.add(
        resp.POST,
        f"http://localhost:9707/{_WS}/api/v1/questionnaires/{_Q_ID}/{_Q_VERSION}/criticalityLevel",
        status=204,
    )

    QuestionnairesApi(responses_client).set_criticality_level(_Q_ID, _Q_VERSION, "Ignore")

    sent = json.loads(resp.calls[0].request.body)
    assert sent["CriticalityLevel"] == "Ignore"
