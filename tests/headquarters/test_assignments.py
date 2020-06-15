from types import GeneratorType
from pytest import fixture, raises
from ssaw import AssignmentsApi
from ssaw.models import Assignment
from ssaw.exceptions import NotFoundError
from . import my_vcr


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
    assert obj.archived == True
    AssignmentsApi(session).unarchive(4)
    obj = AssignmentsApi(session).get_info(4)
    assert obj.archived == False

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
    AssignmentsApi(session).update_recordaudio(4, enabled = not status)
    assert status != AssignmentsApi(session).get_recordaudio(4)
    with raises(TypeError):
        AssignmentsApi(session).update_recordaudio(4, 'enabled')

@my_vcr.use_cassette()
def test_assignment_get_quantity_settings(session):
    assert isinstance(AssignmentsApi(session).get_quantity_settings(4), bool)

@my_vcr.use_cassette()
def test_assignment_assign(session):
    obj = AssignmentsApi(session).assign(4, 'Interviewer1')
    assert obj.responsible == 'Interviewer1'
    with raises(NotFoundError):
        AssignmentsApi(session).assign(4, 'random_user')

@my_vcr.use_cassette()
def test_assignment_get_history(session):
    res = AssignmentsApi(session).get_history(4)
    assert isinstance(res, GeneratorType)
    evnt = next(res)
    assert 'Action' in evnt

@my_vcr.use_cassette()
def test_assignment_create(session, params):
    identifying_data = [
        {"Variable": "address", "Answer": "123 Main Street"},
        {"Variable": "name", "Answer": "Jane Doe"}
    ]
    newobj = Assignment(
        responsible="Interviewer1", 
        questionnaire_id=params['QuestionnaireId'], 
        quantity=5, 
        identifying_data=identifying_data)

    res = AssignmentsApi(session).create(newobj)
    assert res.responsible == "Interviewer1"