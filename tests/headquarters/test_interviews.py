import types

from pytest import raises

from ssaw import InterviewsApi, UsersApi
from ssaw.exceptions import NotAcceptableError, NotFoundError
from ssaw.headquarters_schema import Interview
from ssaw.models import InteriviewHistoryItem
from ssaw.utils import to_hex

from . import my_vcr


@my_vcr.use_cassette(decode_compressed_response=True)
def test_interview_list(session, params):
    large_take = 103
    r = InterviewsApi(session).get_list(take=large_take, questionnaire_id=to_hex(params['TemplateId']))
    assert isinstance(r, types.GeneratorType)
    assert isinstance(next(r), Interview), "There should be a list of Interview objects"
    assert len(list(r)) == large_take - 1, "We have to have all items returned"

    r = list(InterviewsApi(session).get_list(take=2,
                                             order={'created_date': 'ASC'},
                                             fields=['created_date'],
                                             questionnaire_id=to_hex(params['TemplateId'])))
    assert r[0].created_date < r[1].created_date


@my_vcr.use_cassette()
def test_interview_details(session, params):
    """Tests an API call to get an interview details"""

    r = InterviewsApi(session).get_info(params['InterviewId'])
    assert r.get_answer("sex") == "Man"


@my_vcr.use_cassette()
def test_interview_history(session, params):
    """Tests an API call to get an interview history"""

    r = InterviewsApi(session).history(params['InterviewId'])
    assert isinstance(r, types.GeneratorType)
    assert isinstance(next(r), InteriviewHistoryItem), "Should be list of InterviewHistoryItem objects"


@my_vcr.use_cassette()
def test_interview_approve_errors(session, params):
    with raises(NotAcceptableError):
        assert InterviewsApi(session).approve(params['InterviewId'])


@my_vcr.use_cassette()
def test_interview_delete(session):
    with raises(NotFoundError):
        InterviewsApi(session).delete("random string")


@my_vcr.use_cassette()
def test_interview_reject(session, params):
    with raises(NotAcceptableError):
        assert InterviewsApi(session).reject(params['InterviewId'])


@my_vcr.use_cassette()
def test_interview_hqapprove(session, params):
    with raises(NotAcceptableError):
        assert InterviewsApi(session).hqapprove(params['InterviewId'])


@my_vcr.use_cassette()
def test_interview_hqreject(session, params):
    with raises(NotAcceptableError):
        assert InterviewsApi(session).hqreject(params['InterviewId'])


@my_vcr.use_cassette()
def test_interview_hqunapprove(session, params):
    with raises(NotAcceptableError):
        assert InterviewsApi(session).hqunapprove(params['InterviewId'])


@my_vcr.use_cassette()
def test_interview_assign(session, params):
    with raises(NotAcceptableError):
        InterviewsApi(session).assign(params['InterviewId'], '00000000-0000-0000-0000-000000000000')


@my_vcr.use_cassette()
def test_interview_assign_supervisor(session, admin_session):
    sup1 = next(UsersApi(admin_session).get_list(role="SUPERVISOR", take=1))
    interview = next(InterviewsApi(session).get_list(take=1, fields=["id", "key"]))
    InterviewsApi(session).assign_supervisor(interview.id, sup1.id)
    interview = next(InterviewsApi(session).get_list(key=interview.key, fields=["supervisor_name"]))
    assert interview.supervisor_name == sup1.user_name


@my_vcr.use_cassette()
def test_interview_comment(session, params):
    with raises(TypeError):
        InterviewsApi(session).comment(params['InterviewId'], comment="aaa")

    # no way to check comments for now, make sure there are no exceptions
    InterviewsApi(session).comment(params['InterviewId'], comment="aaa", variable="sex")
    InterviewsApi(session).comment(params['InterviewId'], comment="aaa", question_id="fe9719791f0bde796f28d74e66d67d12")

    with raises(NotAcceptableError):
        InterviewsApi(session).comment(params['InterviewId'], comment="aaa", variable="sex", roster_vector=[1])


@my_vcr.use_cassette()
def test_interview_set_get_delete_calendar_event(session):
    api = InterviewsApi(session)
    interview = next(api.get_list(take=1, fields=["key"]))
    api.set_calendar_event(interview.key, "2022-02-03T12:34:34", "EST", "Hello")
    ce = api.get_calendar_event(interview.key)
    assert ce.comment == "Hello"

    api.set_calendar_event(interview.key, "2022-02-03T12:34:34", "EST", "Hello2")
    ce = api.get_calendar_event(interview.key)
    assert ce.comment == "Hello2"

    api.delete_calendar_event(interview.key)
    assert api.get_calendar_event(interview.key).__json_data__ == {}

    with raises(ValueError):
        api.delete_calendar_event("random string")
