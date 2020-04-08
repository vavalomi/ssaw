from os.path import join
from ssaw import ExportApi
from ssaw.exceptions import *
from pytest import raises
from . import my_vcr
import tempfile


@my_vcr.use_cassette()
def test_export_notfound(session):
	with raises(NotFoundError):
		assert ExportApi(session).get_info('00000000-0000-0000-0000-000000000000$1', 'Tabular')

@my_vcr.use_cassette()
def test_export_info(session, params):

	r = ExportApi(session).get_info(params['QuestionnaireId'], 'Tabular')
	assert 'HasExportedFile' in r.keys(), 'Export info response should contain HasExportedFile key'

@my_vcr.use_cassette()
def test_export_cancel(session, params):
	r = ExportApi(session).cancel(params['QuestionnaireId'], 'Tabular')
	assert r == 0

@my_vcr.use_cassette()
def test_export_start(session, params):
	r = ExportApi(session).start(params['QuestionnaireId'], 'Tabular')
	assert r == True

@my_vcr.use_cassette()
def test_export_get(session, params):
	tempdir = tempfile.gettempdir()
	r = ExportApi(session).get(params['QuestionnaireId'], tempdir, 'Tabular')
	assert r == join(tempdir, 'health_survey_1_Tabular_All.zip')