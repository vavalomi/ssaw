from pytest import fixture, raises
from ssaw.headquarters.models import Questionnaire
from ssaw.headquarters.exceptions import IncompleteQuestionnaireIdError
from . import my_vcr


@fixture
def statuses():
	return ['RejectedBySupervisor', 'Completed', 'ApprovedBySupervisor']

@my_vcr.use_cassette()
def test_interview_statuses(session, statuses):
	"""Tests an API call to get interview statuses"""

	response = session.questionnaires.statuses()

	assert isinstance(response, list)
	assert set(statuses).issubset(response), "All keys should be in the response"

@my_vcr.use_cassette()
def test_questionnaire_list(session):
	response = session.questionnaires()
	assert isinstance(response, list)
	assert isinstance(response[0], Questionnaire), "Should be list of Questionnaire objects"

@my_vcr.use_cassette()
def test_questionnaire_incomplete1(session):
	with raises(IncompleteQuestionnaireIdError):
		_ = session.questionnaires(version=3)

@my_vcr.use_cassette()
def test_questionnaire_incomplete2(session):
	with raises(IncompleteQuestionnaireIdError):
		_ = session.questionnaires(id=3)

@my_vcr.use_cassette(decode_compressed_response=True)
def test_questionnaire_single(session, params):
	response = session.questionnaires(params['TemplateId'], params['TemplateVersion'])
	assert response.questionnaire_id == params['TemplateId']


@my_vcr.use_cassette(decode_compressed_response=True)
def test_questionnaire_document(session, params):
	response = session.questionnaires.document(params['TemplateId'], params['TemplateVersion'])
	# this is a json object no easy test for now

@my_vcr.use_cassette()
def test_questionnaire_interviews(session, params):
	response = session.questionnaires.interviews(params['TemplateId'], params['TemplateVersion'])
	assert isinstance(response, dict)
	assert 'Interviews' in response.keys(), "The Interviews should be in the response"
