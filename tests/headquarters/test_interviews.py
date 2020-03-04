import vcr
from pytest import raises
from ssaw.headquarters.exceptions import NotAcceptableError, NotFoundError

my_vcr = vcr.VCR(
    serializer='yaml',
    cassette_library_dir='tests/headquarters/vcr_cassettes',
    path_transformer=vcr.VCR.ensure_suffix('.yaml'),
    record_mode='once',
    filter_headers=[('authorization', None)]
)

@my_vcr.use_cassette(decode_compressed_response=True)
def test_interview_list(session):
    r = session.interviews()
    assert isinstance(r, dict)
    assert 'Interviews' in r.keys(), "The Interviews key should be in the response"

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
    with raises(NotFoundError):
        assert session.interviews.assign(params['InterviewId'], '00000000-0000-0000-0000-000000000000')