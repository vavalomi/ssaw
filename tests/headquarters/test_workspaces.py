from types import GeneratorType
from unittest.mock import Mock

from pytest import mark, raises

from ssaw import UsersApi, WorkspacesApi
from ssaw.exceptions import FeatureNotSupported, ForbiddenError
from ssaw.models import Version, Workspace

from . import my_vcr


@my_vcr.use_cassette()
def test_workspaces_list(session):
    response = WorkspacesApi(session).get_list()
    assert isinstance(response, GeneratorType)
    assert hasattr(next(response), "display_name"), "We should get Workspace objects"

    response = WorkspacesApi(session).get_list(user_id="00000000-0000-0000-0000-000000000000")
    with raises(StopIteration):
        next(response)


@my_vcr.use_cassette()
def test_workspaces_info(session):
    response = WorkspacesApi(session).get_info('primary')
    assert response == Workspace.construct(display_name='Default Workspace', name='primary', disabled_at_utc=None)


@my_vcr.use_cassette()
def test_workspaces_create(admin_session, session):
    response = WorkspacesApi(admin_session).create('new', 'this is new')
    assert response == Workspace.construct(display_name='this is new', name='new', disabled_at_utc=None)
    with raises(ForbiddenError):
        _ = WorkspacesApi(session).create('cannot', 'cannot create as api user')


@my_vcr.use_cassette()
@mark.order(after="test_workspaces_info")
def test_workspaces_update(session):
    response = WorkspacesApi(session).update('primary', 'new description')
    assert response is None


@my_vcr.use_cassette()
def test_workspaces_delete(admin_session):
    _ = WorkspacesApi(admin_session).create('tobedeleted', 'to be deleted')
    response = WorkspacesApi(admin_session).delete('tobedeleted')
    assert response is None


@my_vcr.use_cassette()
def test_workspaces_enable_disable(admin_session):
    _ = WorkspacesApi(admin_session).create('enable', 'to be deleted')
    response = WorkspacesApi(admin_session).disable('enable')
    assert response is None
    response = WorkspacesApi(admin_session).enable('enable')
    assert response is None


@my_vcr.use_cassette()
def test_workspaces_assign(admin_session):
    u = next(UsersApi(admin_session).get_list(role="HEADQUARTER", take=1))
    _ = WorkspacesApi(admin_session).create('assign', 'to be deleted')
    with raises(ValueError):
        _ = WorkspacesApi(admin_session).assign(u.id, 'assign', mode='abc')
    response = WorkspacesApi(admin_session).assign(u.id, 'assign')
    assert response is None


@my_vcr.use_cassette()
def test_workspaces_status(admin_session):
    _ = WorkspacesApi(admin_session).create('status', 'to be deleted')
    response = WorkspacesApi(admin_session).status('status')
    assert hasattr(response, 'can_be_deleted')


def test_workspaces_old_server():
    session_mock = Mock()
    session_mock.version = Version("20.12 (build 29959)")

    with raises(FeatureNotSupported):
        _ = WorkspacesApi(session_mock).get_list()
