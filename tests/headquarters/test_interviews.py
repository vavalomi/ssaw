import types
from pytest import raises
from ssaw import InterviewsApi
from ssaw.exceptions import NotAcceptableError, NotFoundError
from ssaw.headquarters_schema import Interview
from . import my_vcr
from ssaw.utils import to_hex


@my_vcr.use_cassette(decode_compressed_response=True)
def test_interview_list(session, params):
    r = InterviewsApi(session).get_list(questionnaire_id=to_hex(params['TemplateId']))
    assert isinstance(r, types.GeneratorType)
    assert isinstance(next(r), Interview), "There should be a list of Interview objects"

@my_vcr.use_cassette()
def test_interview_details(session, params):
    """Tests an API call to get an interview details"""

    r = InterviewsApi(session).get_info(params['InterviewId'])
    assert 'Answers' in r.keys(), "The Answers key should be in the response"

@my_vcr.use_cassette()
def test_interview_history(session, params):
    """Tests an API call to get an interview history"""

    r = InterviewsApi(session).history(params['InterviewId'])
    assert 'InterviewId' in r.keys(), "The Questions key should be in the response"

@my_vcr.use_cassette()
def test_interview_approve_errors(session, params):
    with raises(NotAcceptableError):
        assert InterviewsApi(session).approve(params['InterviewId'])


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
        assert InterviewsApi(session).assign(params['InterviewId'], '00000000-0000-0000-0000-000000000000')