import types
from pytest import raises
from ssaw.headquarters.exceptions import NotAcceptableError, NotFoundError
from ssaw.headquarters.models import InterviewListItem
from . import my_vcr


@my_vcr.use_cassette(decode_compressed_response=True)
def test_interview_list(session):
    r = session.interviews.get_list()
    assert isinstance(r, types.GeneratorType)
    assert isinstance(next(r), InterviewListItem), "There should be a list of InterviewListItem objects"

@my_vcr.use_cassette()
def test_interview_details(session, params):
    """Tests an API call to get an interview details"""

    r = session.interviews.get_info(params['InterviewId'])
    assert 'Answers' in r.keys(), "The Answers key should be in the response"

@my_vcr.use_cassette()
def test_interview_history(session, params):
    """Tests an API call to get an interview history"""

    r = session.interviews.history(params['InterviewId'])
    assert 'InterviewId' in r.keys(), "The Questions key should be in the response"

@my_vcr.use_cassette()
def test_interview_approve_errors(session, params):
    with raises(NotAcceptableError):
        assert session.interviews.approve(params['InterviewId'])


@my_vcr.use_cassette()
def test_interview_reject(session, params):
    with raises(NotAcceptableError):
        assert session.interviews.reject(params['InterviewId'])

@my_vcr.use_cassette()
def test_interview_hqapprove(session, params):
    with raises(NotAcceptableError):
        assert session.interviews.hqapprove(params['InterviewId'])


@my_vcr.use_cassette()
def test_interview_hqreject(session, params):
    with raises(NotAcceptableError):
        assert session.interviews.hqreject(params['InterviewId'])

@my_vcr.use_cassette()
def test_interview_hqunapprove(session, params):
    with raises(NotAcceptableError):
        assert session.interviews.hqunapprove(params['InterviewId'])

@my_vcr.use_cassette()
def test_interview_assign(session, params):
    with raises(NotAcceptableError):
        assert session.interviews.assign(params['InterviewId'], '00000000-0000-0000-0000-000000000000')