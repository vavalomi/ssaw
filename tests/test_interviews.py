import vcr

my_vcr = vcr.VCR(
	serializer='yaml',
	cassette_library_dir='tests/vcr_cassettes',
	path_transformer=vcr.VCR.ensure_suffix('.yaml'),
	record_mode='once',
	filter_headers=[('authorization', None)]
)

@my_vcr.use_cassette(decode_compressed_response=True)
def test_interview_list(session):
	r = session.Interviews.All()
	assert isinstance(r, dict)
	assert 'Interviews' in r.keys(), "The Interviews key should be in the response"

@my_vcr.use_cassette()
def test_interview_details(session, params):
	"""Tests an API call to get an interview details"""

	r = session.Interviews.Details(params['InterviewId'])
	assert 'Questions' in r.keys(), "The Questions key should be in the response"

@my_vcr.use_cassette()
def test_interview_history(session, params):
	"""Tests an API call to get an interview history"""

	r = session.Interviews.History(params['InterviewId'])
	assert 'InterviewId' in r.keys(), "The Questions key should be in the response"

@my_vcr.use_cassette()
def test_interview_approve(session, params):
	r = session.Interviews.Approve(params['InterviewId'])
	assert r == False, "did we approve something?"

@my_vcr.use_cassette()
def test_interview_reject(session, params):
	r = session.Interviews.Reject(params['InterviewId'])
	assert r == True, "did we reject something?"

@my_vcr.use_cassette()
def test_interview_hqapprove(session, params):
	r = session.Interviews.HQApprove(params['InterviewId'])
	assert r == False, "did we hqapprove something?"

@my_vcr.use_cassette()
def test_interview_hqreject(session, params):
	r = session.Interviews.HQReject(params['InterviewId'])
	assert r == False, "did we hqreject something?"

@my_vcr.use_cassette()
def test_interview_hqunapprove(session, params):
	r = session.Interviews.HQUnapprove(params['InterviewId'])
	assert r == False, "did we hqunapprove something?"

@my_vcr.use_cassette()
def test_interview_assign(session, params):
	r = session.Interviews.Assign(params['InterviewId'], '00000000-0000-0000-0000-000000000000')
	assert r == False, "did we reassign something?"