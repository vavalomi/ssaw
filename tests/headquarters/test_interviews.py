import types

from pytest import raises

from ssaw import InterviewsApi
from ssaw.exceptions import NotAcceptableError
from ssaw.headquarters_schema import Interview
from ssaw.utils import to_hex

from . import my_vcr


@my_vcr.use_cassette(decode_compressed_response=True)
def test_interview_list(session, params):
    r = InterviewsApi(session).get_list(questionnaire_id=to_hex(params['TemplateId']))
    assert isinstance(r, types.GeneratorType)
    assert isinstance(next(r), Interview), "There should be a list of Interview objects"


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
    assert 'Action' in next(r).keys(), "The actions should be in the response"


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
        InterviewsApi(session).assign(params['InterviewId'], '00000000-0000-0000-0000-000000000000')


@my_vcr.use_cassette()
def test_interview_comment(session, params):
    with raises(TypeError):
        InterviewsApi(session).comment(params['InterviewId'], comment="aaa")

    # no way to check comments for now, make sure there are no exceptions
    InterviewsApi(session).comment(params['InterviewId'], comment="aaa", variable="sex")
