import types
from pytest import fixture, raises
from ssaw import AssignmentsApi
from ssaw.models import Assignment
from ssaw.exceptions import NotFoundError
from . import my_vcr


@my_vcr.use_cassette()
def test_assignment_list(session):
    response = AssignmentsApi(session).get_list()
    assert isinstance(response, types.GeneratorType), "Should be a generator"
    assert isinstance(next(response), Assignment), "Should be list of Assignment objects"

@my_vcr.use_cassette()
def test_assignment_details(session):
    """Tests an API call to get an assignment details"""

    response = AssignmentsApi(session).get_info(2)

    assert isinstance(response, Assignment)
    assert response.id == 2, "The ID should be in the response"

@my_vcr.use_cassette()
def test_assignment_details_notfound(session):
    """Tests an API call to get an assignment details with incorrect id"""

    with raises(NotFoundError):
        assert AssignmentsApi(session).get_info(7373)

