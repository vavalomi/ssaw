
from datetime import datetime
from types import GeneratorType

from pytest import raises

from ssaw import UsersApi
from ssaw.exceptions import GraphQLError
from ssaw.headquarters_schema import User as GraphQLUser

from . import my_vcr
from ..utils import random_name


@my_vcr.use_cassette()
def test_user_list(admin_session):
    response = UsersApi(admin_session).get_list()
    assert isinstance(response, GeneratorType)
    assert isinstance(next(response), GraphQLUser), "Should be list of User objects"
    assert len(list(response)) == 109, "We have to have all items returned"

    first_user = next(UsersApi(admin_session).get_list(order=['creation_date'], take=1))
    assert first_user.role == 'ADMINISTRATOR'


@my_vcr.use_cassette()
def test_user_create(session):
    ret = UsersApi(session).create(user_name=random_name(), password="Validpassword1", role="Supervisor")
    assert "UserId" in ret.keys(), "Id of the create user must be returned"


@my_vcr.use_cassette()
def test_supervisor_list(session):
    response = UsersApi(session).list_supervisors()
    assert isinstance(response, GeneratorType)
    assert 'UserName' in next(response).keys(), "The UserName should be in the response"
    assert len(list(response)) >= 13, "We have to have all items returned"


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


@my_vcr.use_cassette()
def test_user_viewer(session):
    res = UsersApi(session).viewer()
    assert res.role == "APIUSER"

    res = UsersApi(session).viewer("inter1", "Validpassword1")
    assert res.role == "INTERVIEWER"
    assert res.id == "f6aefcabe847413aade21a29b4d4af39"


@my_vcr.use_cassette(filter_post_data_parameters=["UserName", "Password"])
def test_user_lock_unlock(session, admin_session):
    with raises(GraphQLError) as e_info:
        UsersApi(session).lock("inter1")
    assert "The current user is not authorized to access this resource" in str(e_info.value)

    api = UsersApi(admin_session)
    with raises(ValueError):
        api.lock()

    api.lock("inter1")
    assert next(api.get_list(fields=["is_locked"], user_name="inter1")).is_locked is True
    api.unlock(user_id="0ab27c3a-217f-46f7-8aed-ffa7cd88a412")
    assert next(api.get_list(fields=["is_locked"], user_name="inter1")).is_locked is False


@my_vcr.use_cassette(filter_post_data_parameters=["UserName", "Password"])
def test_user_change_password(session, admin_session):
    with raises(GraphQLError) as e_info:
        UsersApi(session).change_password(user_name="inter1", password="123")
    assert "The current user is not authorized to access this resource" in str(e_info.value)

    UsersApi(admin_session).change_password(user_name="inter1", password="Password12345")

    with raises(GraphQLError) as e_info:
        UsersApi(session).viewer("inter1", "Password12345")
