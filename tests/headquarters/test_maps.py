import types
from unittest.mock import Mock

from pytest import raises

from ssaw import MapsApi
from ssaw.exceptions import NotAcceptableError
from ssaw.headquarters_schema import Map
from ssaw.models import Version

from . import my_vcr


@my_vcr.use_cassette()
def test_map_list(session):
    r = MapsApi(session).get_list()
    assert isinstance(r, types.GeneratorType)
    assert isinstance(next(r), Map), "There should be a list of Map objects"

    r = MapsApi(session).get_list(take=1, order=["file_name"])
    assert next(r).file_name == "map2.tpk", "The first element must be map2.tpk"
    with raises(StopIteration):
        next(r)

    m = next(MapsApi(session).get_list(skip=1, order=["file_name"]))
    assert m.file_name == "map.tpk", "After skipping one, the first element must be map.tpk"

    r = MapsApi(session).get_list(filter_user="random")
    with raises(StopIteration):
        next(r)


@my_vcr.use_cassette()
def test_map_delete(session, params):
    r = MapsApi(session).delete(params["MapFileName2"])
    assert isinstance(r, Map)


@my_vcr.use_cassette()
def test_map_upload(admin_session, params):
    r = MapsApi(admin_session).upload(params["MapsArchive"])
    assert r is True

    with raises(NotAcceptableError):
        _ = MapsApi(admin_session).upload(__file__)


@my_vcr.use_cassette()
def test_map_add_user(session, params):
    r = MapsApi(session).add_user(params["MapFileName"], params["MapUserName"])
    assert isinstance(r, Map)


@my_vcr.use_cassette()
def test_map_delete_user(session, params):
    r = MapsApi(session).delete_user(params["MapFileName"], params["MapUserName"])
    assert isinstance(r, Map)


def test_map_default_fields():
    session_mock = Mock()
    session_mock.version = Version("20.12 (build 29959)")

    assert MapsApi(session_mock)._default_fields() == ["file_name", "import_date", ]
