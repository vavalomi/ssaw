from headquarters.utils import *
import pytest
import vcr
import tempfile

my_vcr = vcr.VCR(
	serializer='yaml',
	cassette_library_dir='tests/vcr_cassettes',
	path_transformer=vcr.VCR.ensure_suffix('.yaml'),
	record_mode='once',
	filter_headers=[('authorization', None)]
)

@my_vcr.use_cassette()
def test_export_notfound(session):
	with pytest.raises(NotFoundError):
		r = session.Export.GetInfo('00000000-0000-0000-0000-000000000000$1', 'Tabular')

@my_vcr.use_cassette()
def test_export_info(session, params):

	r = session.Export.GetInfo(params['QuestionnaireId'], 'Tabular')
	assert 'HasExportedFile' in r.keys(), 'Export info response should contain HasExportedFile key'

@my_vcr.use_cassette()
def test_export_cancel(session, params):
	r = session.Export.Cancel(params['QuestionnaireId'], 'Tabular')
	assert r == 0

@my_vcr.use_cassette()
def test_export_start(session, params):
	r = session.Export.Start(params['QuestionnaireId'], 'Tabular')
	assert r == 200

@my_vcr.use_cassette()
def test_export_get(session, params):
	tempdir = tempfile.gettempdir()
	r = session.Export.Get(params['QuestionnaireId'], tempdir, 'Tabular')
	assert r == tempdir + '/Copy+of+SM_1_Tabular_All.zip'