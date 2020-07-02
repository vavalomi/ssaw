import types

from ssaw import UsersApi

from . import my_vcr


@my_vcr.use_cassette()
def test_supervisor_list(session):
    response = UsersApi(session).list_supervisors()
    assert isinstance(response, types.GeneratorType)
    assert 'UserName' in next(response).keys(), "The UserName should be in the response"


@my_vcr.use_cassette()
def test_interviewer_list(session, params):
    response = UsersApi(session).list_interviewers(params['SupervisorId'])
    assert 'UserName' in next(response).keys(), "The UserName should be in the response"


@my_vcr.use_cassette()
def test_user_info(session, params):
    response = UsersApi(session).get_info(params['SupervisorId'])
    assert isinstance(response, dict)
    assert response['UserId'] == params['SupervisorId'], "The userid should be in the response"


@my_vcr.use_cassette()
def test_user_archive(session, params):
    response = UsersApi(session).archive(params['SupervisorId'])
    assert response is True, "did we archive someone?"


@my_vcr.use_cassette()
def test_user_unarchive(session, params):
    response = UsersApi(session).unarchive(params['SupervisorId'])
    assert response is True, "did we unarchive someone?"
