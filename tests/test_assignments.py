from pytest import fixture
import vcr

my_vcr = vcr.VCR(
	serializer='yaml',
	cassette_library_dir='tests/vcr_cassettes',
	path_transformer=vcr.VCR.ensure_suffix('.yaml'),
	record_mode='once',
	filter_headers=[('authorization', None)]
)

@fixture
def assignment_keys():
	return ['Id', 'ResponsibleId', 'ResponsibleName', 'QuestionnaireId',
		'InterviewsCount', 'Quantity', 'Archived',
		'CreatedAtUtc', 'UpdatedAtUtc', 'IdentifyingData', 'Answers']

@my_vcr.use_cassette()
def test_assignment_details(session, assignment_keys):
	"""Tests an API call to get an assignment details"""

	response = session.Assignments(7373)

	assert isinstance(response, dict)
	assert response['Id'] == 7373, "The ID should be in the response"
	assert set(assignment_keys) == set(response.keys()), "All keys should be in the response"

@my_vcr.use_cassette()
def test_assignment_list(session):
	response = session.Assignments()
	assert isinstance(response, dict)
	assert 'Assignments' in response.keys(), "The Assignments should be in the response"
