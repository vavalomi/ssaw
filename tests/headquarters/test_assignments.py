from pytest import fixture, raises
from ssaw.headquarters.models import Assignment
from ssaw.headquarters.exceptions import NotFoundError
from . import my_vcr

@fixture
def assignment_keys():
    return ['Id', 'ResponsibleId', 'ResponsibleName', 'QuestionnaireId',
        'InterviewsCount', 'Quantity', 'Archived',
        'CreatedAtUtc', 'UpdatedAtUtc', 'IdentifyingData', 'Answers',
        'Email', 'Password', 'IdentifyingQuestions', 'WebMode']

@my_vcr.use_cassette()
def test_assignment_list(session):
    response = session.assignments()
    print(response)
    assert isinstance(response, list), "Should be of type list"
    assert isinstance(response[0], Assignment), "Should be list of Assignment objects"

@my_vcr.use_cassette()
def test_assignment_details(session, assignment_keys):
    """Tests an API call to get an assignment details"""

    response = session.assignments.get_info(2)

    assert isinstance(response, dict)
    assert response['Id'] == 2, "The ID should be in the response"
    assert set(assignment_keys) == set(response.keys()), "All keys should be in the response"

@my_vcr.use_cassette()
def test_assignment_details_notfound(session, assignment_keys):
    """Tests an API call to get an assignment details with incorrect id"""

    with raises(NotFoundError):
        assert session.assignments.get_info(7373)

