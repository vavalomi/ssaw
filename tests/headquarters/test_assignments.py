from types import GeneratorType

from pytest import raises

from ssaw import AssignmentsApi
from ssaw.exceptions import NotFoundError
from ssaw.models import Assignment

from . import my_vcr
from ..utils import create_assignment


@my_vcr.use_cassette()
def test_assignment_list(session, params):
    response = AssignmentsApi(session).get_list(params['TemplateId'], params['TemplateVersion'])
    assert isinstance(response, GeneratorType), "Should be a generator"
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


@my_vcr.use_cassette()
def test_assignment_archive_unarchive(session):
    AssignmentsApi(session).archive(4)
    obj = AssignmentsApi(session).get_info(4)
    assert obj.archived is True
    AssignmentsApi(session).unarchive(4)
    obj = AssignmentsApi(session).get_info(4)
    assert obj.archived is False


@my_vcr.use_cassette()
def test_assignment_update_quantity(session):
    obj = AssignmentsApi(session).get_info(4)
    quantity = obj.quantity
    obj = AssignmentsApi(session).update_quantity(obj.id, quantity + 1)
    obj = AssignmentsApi(session).get_info(obj.id)
    assert obj.quantity == quantity + 1
    with raises(TypeError):
        AssignmentsApi(session).update_quantity(obj.id, 'quantity')


@my_vcr.use_cassette()
def test_assignment_close(session):
    obj = AssignmentsApi(session).get_info(4)
    _ = AssignmentsApi(session).update_quantity(obj.id, obj.quantity + 1)
    AssignmentsApi(session).close(obj.id)
    obj = AssignmentsApi(session).get_info(obj.id)
    assert obj.interviews_count == obj.quantity


@my_vcr.use_cassette()
def test_assignment_update_recordaudio(session):
    status = AssignmentsApi(session).get_recordaudio(4)
    AssignmentsApi(session).update_recordaudio(4, enabled=not status)
    assert status != AssignmentsApi(session).get_recordaudio(4)
    with raises(TypeError):
        AssignmentsApi(session).update_recordaudio(4, 'enabled')


@my_vcr.use_cassette()
def test_assignment_get_quantity_settings(session):
    assert isinstance(AssignmentsApi(session).get_quantity_settings(4), bool)


@my_vcr.use_cassette()
def test_assignment_assign(session):
    obj = AssignmentsApi(session).assign(2, 'inter2')
    assert obj.responsible == 'inter2'
    with raises(NotFoundError):
        AssignmentsApi(session).assign(4, 'random_user')


@my_vcr.use_cassette()
def test_assignment_get_history(session):
    res = AssignmentsApi(session).get_history(2)
    assert isinstance(res, GeneratorType)
    evnt = next(res)
    assert hasattr(evnt, "action")


@my_vcr.use_cassette()
def test_assignment_create(session, params):
    identifying_data = [
        {"Variable": "address", "Answer": "123 Main Street"},
        {"Variable": "name", "Answer": "Jane Doe"}
    ]

    res = create_assignment(session, "inter1", params['QuestionnaireId'], identifying_data)

    assert res.responsible == "inter1"
    assert res.identifying_data[0]["Answer"] == identifying_data[0]["Answer"]


@my_vcr.use_cassette()
def test_assignment_set_get_delete_calendar_event(session):
    api = AssignmentsApi(session)
    assignment = next(api._get_list(take=1, fields=["id"]))
    api.set_calendar_event(assignment.id, "2022-02-03T12:34:34", "EST", "Hello")
    ce = api.get_calendar_event(assignment.id)
    assert ce.comment == "Hello"

    api.set_calendar_event(assignment.id, "2022-02-03T12:34:34", "EST", "Hello2")
    ce = api.get_calendar_event(assignment.id)
    assert ce.comment == "Hello2"

    api.delete_calendar_event(assignment.id)
    assert api.get_calendar_event(assignment.id).__json_data__ == {}

    with raises(ValueError):
        api.delete_calendar_event("random string")
