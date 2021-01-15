import types

from pytest import raises

from ssaw import MapsApi
from ssaw.headquarters_schema import Map

from . import my_vcr


@my_vcr.use_cassette()
def test_map_list(session):
    r = MapsApi(session).get_list()
    assert isinstance(r, types.GeneratorType)
    assert isinstance(next(r), Map), "There should be a list of Map objects"

    r = MapsApi(session).get_list(filter_user="random")
    with raises(StopIteration):
        next(r)


@my_vcr.use_cassette()
def test_map_delete(session, params):
    r = MapsApi(session).delete(params["MapFileName2"])
    assert isinstance(r, Map)


@my_vcr.use_cassette()
def test_map_add_user(session, params):
    r = MapsApi(session).add_user(params["MapFileName"], params["MapUserName"])
    assert isinstance(r, Map)


@my_vcr.use_cassette()
def test_map_delete_user(session, params):
    r = MapsApi(session).delete_user(params["MapFileName"], params["MapUserName"])
    assert isinstance(r, Map)
