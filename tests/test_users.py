from pytest import fixture
import vcr

my_vcr = vcr.VCR(
	serializer='yaml',
	cassette_library_dir='tests/vcr_cassettes',
	path_transformer=vcr.VCR.ensure_suffix('.yaml'),
	record_mode='once',
	filter_headers=[('authorization', None)]
)

@my_vcr.use_cassette()
def test_supervisor_list(session):
	response = session.Users.AllSupervisors()
	assert isinstance(response, dict)
	assert 'Users' in response.keys(), "The Users should be in the response"

@my_vcr.use_cassette()
def test_interviewer_list(session, params):
	response = session.Users.AllInterviewers(params['SupervisorId'])
	assert isinstance(response, dict)
	assert 'Users' in response.keys(), "The Users should be in the response"


@my_vcr.use_cassette()
def test_user_info(session, params):
	response = session.Users.GetInfo(params['SupervisorId'])
	assert isinstance(response, dict)
	assert response['UserId'] == params['SupervisorId'], "The userid should be in the response"

@my_vcr.use_cassette()
def test_user_archive(session, params):
	response = session.Users.Archive(params['SupervisorId'])
	assert response == 200, "did we archive someone?"


@my_vcr.use_cassette()
def test_user_unarchive(session, params):
	response = session.Users.Unarchive(params['SupervisorId'])
	assert response == 200, "did we unarchive someone?"
