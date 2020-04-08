import types
from pytest import fixture, raises
from ssaw import QuestionnairesApi
from ssaw.models import QuestionnaireListItem
from ssaw.exceptions import IncompleteQuestionnaireIdError
from . import my_vcr


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
def test_questionnaire_list(session):
	response = QuestionnairesApi(session).get_list()
	assert isinstance(response, types.GeneratorType)
	assert isinstance(next(response), QuestionnaireListItem), "Should be list of Questionnaire objects"

@my_vcr.use_cassette(decode_compressed_response=True)
def test_questionnaire_document(session, params):
	response = QuestionnairesApi(session).document(params['TemplateId'], params['TemplateVersion'])
	# this is a json object no easy test for now

@my_vcr.use_cassette()
def test_questionnaire_interviews(session, params):
	response = QuestionnairesApi(session).interviews(params['TemplateId'], params['TemplateVersion'])
	assert isinstance(response, dict)
	assert 'Interviews' in response.keys(), "The Interviews should be in the response"
