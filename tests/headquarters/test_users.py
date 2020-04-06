import types
from pytest import fixture
from . import my_vcr


@my_vcr.use_cassette()
def test_supervisor_list(session):
    response = session.users.list_supervisors()
    assert isinstance(response, types.GeneratorType)
    assert 'UserName' in next(response).keys(), "The UserName should be in the response"

@my_vcr.use_cassette()
def test_interviewer_list(session, params):
    response = session.users.list_interviewers(params['SupervisorId'])
    assert 'UserName' in next(response).keys(), "The UserName should be in the response"

@my_vcr.use_cassette()
def test_user_info(session, params):
    response = session.users.get_info(params['SupervisorId'])
    assert isinstance(response, dict)
    assert response['UserId'] == params['SupervisorId'], "The userid should be in the response"

@my_vcr.use_cassette()
def test_user_archive(session, params):
    response = session.users.archive(params['SupervisorId'])
    assert response == True, "did we archive someone?"


@my_vcr.use_cassette()
def test_user_unarchive(session, params):
    response = session.users.unarchive(params['SupervisorId'])
    assert response == True, "did we unarchive someone?"
