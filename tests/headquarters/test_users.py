
from datetime import datetime
from types import GeneratorType

from pytest import raises

from ssaw import UsersApi
from ssaw.models import InterviewerAction

from tests.utils import random_name
from . import my_vcr


@my_vcr.use_cassette()
def test_user_create(session):
    ret = UsersApi(session).create(user_name=random_name(), password="Validpassword1", role="Supervisor")
    assert "UserId" in ret.keys(), "Id of the create user must be returned"

@my_vcr.use_cassette()
def test_supervisor_list(session):
    response = UsersApi(session).list_supervisors()
    assert isinstance(response, GeneratorType)
    assert 'UserName' in next(response).keys(), "The UserName should be in the response"


@my_vcr.use_cassette()
def test_interviewer_list(session, params):
    response = UsersApi(session).list_interviewers(params["SupervisorId"])
    assert 'UserName' in next(response).keys(), "The UserName should be in the response"


@my_vcr.use_cassette()
def test_interviewer_emptylist(session):
    random_guid = "767ca045-45e7-4607-9799-29837d87d1d1"
    response = UsersApi(session).list_interviewers(random_guid)
    with raises(StopIteration):
        next(response)


@my_vcr.use_cassette()
def test_user_info(session, params):
    response = UsersApi(session).get_info(params["InterviewerId"])
    assert isinstance(response, dict)
    assert response['UserName'] == "inter1", "The user_name should be the same"


@my_vcr.use_cassette()
def test_user_archive_unarchive(session, params):
    _ = UsersApi(session).archive(params["InterviewerId2"])
    response = UsersApi(session).get_info(params["InterviewerId2"])
    assert response["IsArchived"] is True, "did we archive someone?"

    _ = UsersApi(session).unarchive(params["InterviewerId2"])
    response = UsersApi(session).get_info(params["InterviewerId2"])
    assert response["IsArchived"] is False, "did we unarchive someone?"


@my_vcr.use_cassette()
def test_user_actions_log(session, params):
    """ for now don't have test data with actual actions log
    response = UsersApi(session).get_actions_log(
        params['InterviewerId'], start=datetime(2020, 7, 14), end=datetime(2020, 8, 14))
    assert isinstance(next(response), InterviewerAction)
    """

    response = UsersApi(session).get_actions_log(
        params['InterviewerId'], start=datetime(2000, 7, 14), end=datetime(2000, 8, 14))
    with raises(StopIteration):
        next(response)