from os.path import join
from ssaw.headquarters.exceptions import *
from pytest import raises
import vcr
import tempfile

my_vcr = vcr.VCR(
	serializer='yaml',
	cassette_library_dir='tests/headquarters/vcr_cassettes',
	path_transformer=vcr.VCR.ensure_suffix('.yaml'),
	record_mode='once',
	filter_headers=[('authorization', None)]
)

@my_vcr.use_cassette()
def test_export_notfound(session):
	with raises(NotFoundError):
		assert session.export.get_info('00000000-0000-0000-0000-000000000000$1', 'Tabular')

@my_vcr.use_cassette()
def test_export_info(session, params):

	r = session.export.get_info(params['QuestionnaireId'], 'Tabular')
	assert 'HasExportedFile' in r.keys(), 'Export info response should contain HasExportedFile key'

@my_vcr.use_cassette()
def test_export_cancel(session, params):
	r = session.export.cancel(params['QuestionnaireId'], 'Tabular')
	assert r == 0

@my_vcr.use_cassette()
def test_export_start(session, params):
	r = session.export.start(params['QuestionnaireId'], 'Tabular')
	assert r == True

@my_vcr.use_cassette()
def test_export_get(session, params):
	tempdir = tempfile.gettempdir()
	r = session.export.get(params['QuestionnaireId'], tempdir, 'Tabular')
	assert r == join(tempdir, 'health_survey_1_Tabular_All.zip')