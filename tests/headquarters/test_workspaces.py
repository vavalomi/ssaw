import pytest
from pytest import raises
from types import GeneratorType

from ssaw import UsersApi, WorkspacesApi
from ssaw.exceptions import ForbiddenError

from tests.utils import random_name
from . import my_vcr


@pytest.fixture(scope="module")
def test_workspace(admin_session):
    name = random_name()
    _ = WorkspacesApi(admin_session).create(name, 'test workspace')
    return name


@my_vcr.use_cassette()
def test_workspaces_list(session):
    response = WorkspacesApi(session).get_list()
    assert isinstance(response, GeneratorType)
    assert "DisplayName" in next(response).keys(), "DisplayName should be in the response"

@my_vcr.use_cassette()
def test_workspaces_info(session):
    response = WorkspacesApi(session).get_info('primary')
    assert response == {'DisplayName': 'Default Workspace', 'Name': 'primary', 'DisabledAtUtc': None}

@my_vcr.use_cassette()
def test_workspaces_create(admin_session, session):
    response = WorkspacesApi(admin_session).create('new', 'this is new')
    assert response == {'DisplayName': 'this is new', 'Name': 'new', 'DisabledAtUtc': None}
    with raises(ForbiddenError):
        _ = WorkspacesApi(session).create('cannot', 'cannot create as api user')

@my_vcr.use_cassette()
def test_workspaces_update(session):
    response = WorkspacesApi(session).update('primary', 'new description')
    assert response is True

@my_vcr.use_cassette()
def test_workspaces_delete(admin_session):
    _ = WorkspacesApi(admin_session).create('tobedeleted', 'to be deleted')
    response = WorkspacesApi(admin_session).delete('tobedeleted')
    assert response is True

@my_vcr.use_cassette()
def test_workspaces_enable_disable(admin_session):
    _ = WorkspacesApi(admin_session).create('enable', 'to be deleted')
    response = WorkspacesApi(admin_session).disable('enable')
    assert response is True
    response = WorkspacesApi(admin_session).enable('enable')
    assert response is True

@my_vcr.use_cassette()
def test_workspaces_assign(admin_session, params, test_workspace):
    response = WorkspacesApi(admin_session).assign(params['Headquarters'], test_workspace)
    assert response is True

@my_vcr.use_cassette()
def test_workspaces_status(admin_session, test_workspace):
    response = WorkspacesApi(admin_session).status(test_workspace)
    assert 'CanBeDeleted' in response.keys()