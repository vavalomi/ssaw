import types
from os.path import join
from tempfile import gettempdir
from uuid import UUID

from pytest import fixture

from ssaw import QuestionnairesApi
from ssaw.headquarters_schema import Interview, Questionnaire

from . import my_vcr
from ..utils import create_assignment


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
    response = QuestionnairesApi(session).get_list()
    assert isinstance(response, types.GeneratorType)
    assert isinstance(next(response), Questionnaire), "Should be list of Questionnaire objects"
    assert len(list(response)) == 12, "We have to have all items returned"

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
    assert response is True


@my_vcr.use_cassette()
def test_questionnaire_download_weblinks(admin_session, params):
    _ = create_assignment(admin_session, "inter1", params['QuestionnaireId'], identifying_data=[], webmode=True)
    response = QuestionnairesApi(admin_session).download_web_links(params['TemplateId'], params['TemplateVersion'])
    assert hasattr(response[0], "link")

    tempdir = gettempdir()
    response = QuestionnairesApi(admin_session).download_web_links(params['TemplateId'],
                                                                   params['TemplateVersion'], path=tempdir)
    assert response == join(tempdir, "Web ssaw package test questionnaire (ver. 1).zip")
