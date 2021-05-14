from os.path import join
from tempfile import gettempdir

from pytest import raises

from ssaw import ExportApi
from ssaw.exceptions import NotFoundError
from ssaw.models import ExportJob

from . import my_vcr


@my_vcr.use_cassette()
def test_export_notfound(session):
    with raises(NotFoundError):
        assert ExportApi(session).get_info(123)


@my_vcr.use_cassette()
def test_export_info(session):

    r = ExportApi(session).get_info(1)
    assert isinstance(r, ExportJob), 'Should get back an ExportJob object'
    assert r.job_id == 1, "Should get back the same job id"


@my_vcr.use_cassette()
def test_export_start_cancel(session, params):
    job = ExportJob(params['QuestionnaireId'], export_type="Paradata")
    r = ExportApi(session).start(job)
    assert isinstance(r, ExportJob), "Should get back the created job"
    r = ExportApi(session).cancel(r.job_id)
    assert r is None, 'Does not return anything'


@my_vcr.use_cassette()
def test_export_get(session, params):
    tempdir = gettempdir()
    r = ExportApi(session).get(questionnaire_identity=params['QuestionnaireId'],
                               export_path=tempdir, export_type='Tabular')
    assert r == join(tempdir, 'ssaw_1_Tabular_All.zip')

    r = ExportApi(session).get(questionnaire_identity=params['QuestionnaireId'],
                               export_path=tempdir, export_type='SPSS')

    assert r is None
