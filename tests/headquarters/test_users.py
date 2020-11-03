
from datetime import datetime
from types import GeneratorType

from pytest import raises

from ssaw import UsersApi
from ssaw.models import InterviewerAction

from . import my_vcr


@my_vcr.use_cassette()
def test_supervisor_list(session):
    response = UsersApi(session).list_supervisors()
    assert isinstance(response, GeneratorType)
    assert 'UserName' in next(response).keys(), "The UserName should be in the response"


@my_vcr.use_cassette()
def test_interviewer_list(session, params):
    response = UsersApi(session).list_interviewers(params['SupervisorId'])
    assert 'UserName' in next(response).keys(), "The UserName should be in the response"


@my_vcr.use_cassette()
def test_interviewer_emptylist(session, params):
    response = UsersApi(session).list_interviewers(params['SupervisorId_empty'])
    with raises(StopIteration):
        next(response)


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


@my_vcr.use_cassette()
def test_user_actions_log(session, params):
    response = UsersApi(session).get_actions_log(
        params['InterviewerId'], start=datetime(2020, 7, 14), end=datetime(2020, 8, 14))
    assert isinstance(next(response), InterviewerAction)
