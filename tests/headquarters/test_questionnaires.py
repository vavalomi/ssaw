from pytest import fixture, raises
import vcr
from ssaw.headquarters.utils import IncompleteQuestionnaireIdError


my_vcr = vcr.VCR(
	serializer='yaml',
	cassette_library_dir='tests/headquarters/vcr_cassettes',
	path_transformer=vcr.VCR.ensure_suffix('.yaml'),
	record_mode='once',
	filter_headers=[('authorization', None)]
)

@fixture
def statuses():
	return ['RejectedBySupervisor', 'Completed', 'ApprovedBySupervisor']

@my_vcr.use_cassette()
def test_interview_statuses(session, statuses):
	"""Tests an API call to get interview statuses"""

	response = session.Questionnaires.Statuses()

	assert isinstance(response, list)
	assert set(statuses).issubset(response), "All keys should be in the response"

@my_vcr.use_cassette()
def test_questionnaire_list(session):
	response = session.Questionnaires()
	assert isinstance(response, dict)
	assert 'Questionnaires' in response.keys(), "The Questionnaires should be in the response"

@my_vcr.use_cassette()
def test_questionnaire_incomplete1(session):
	with raises(IncompleteQuestionnaireIdError):
		response = session.Questionnaires(version=3)

@my_vcr.use_cassette()
def test_questionnaire_incomplete2(session):
	with raises(IncompleteQuestionnaireIdError):
		response = session.Questionnaires(id=3)

@my_vcr.use_cassette(decode_compressed_response=True)
def test_questionnaire_single(session, params):
	response = session.Questionnaires(params['TemplateId'], params['TemplateVersion'])
	assert isinstance(response, dict)


@my_vcr.use_cassette(decode_compressed_response=True)
def test_questionnaire_document(session, params):
	response = session.Questionnaires.Document(params['TemplateId'], params['TemplateVersion'])
	# this is a json object no easy test for now

@my_vcr.use_cassette()
def test_questionnaire_interviews(session, params):
	response = session.Questionnaires.Interviews(params['TemplateId'], params['TemplateVersion'])
	assert isinstance(response, dict)
	assert 'Interviews' in response.keys(), "The Interviews should be in the response"
