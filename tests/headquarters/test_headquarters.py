from uuid import UUID

from pytest import raises

from ssaw import Client, MapsApi, QuestionnairesApi
from ssaw.exceptions import GraphQLError, IncompleteQuestionnaireIdError, UnauthorizedError
from ssaw.utils import fix_qid, parse_qidentity

from . import my_vcr


@my_vcr.use_cassette()
def test_headquarters_unathorized():
    s = Client('https://demo.mysurvey.solutions/', "aa", "")

    with raises(UnauthorizedError):
        next(QuestionnairesApi(s).get_list())


@my_vcr.use_cassette()
def test_headquarters_graphql_error():
    s = Client('https://demo.mysurvey.solutions/', "aa", "")

    with raises(GraphQLError):
        next(MapsApi(s).get_list())


def test_utils_parse_qidentity(params):

    a = parse_qidentity(params["QuestionnaireId"])
    assert a == params["QuestionnaireId"].replace("-", ""), "UUID in hex format $ version"

    with raises(IncompleteQuestionnaireIdError):
        parse_qidentity(params["TemplateId"])

    a = parse_qidentity((params["TemplateId"], 1))
    assert a == "{}${}".format(UUID(params["TemplateId"]).hex, 1)


def test_utils_fix_qid(params):

    def foo(interview_id):
        return interview_id

    assert fix_qid(expects={'interview_id': 'hex'})(foo)(
        interview_id=params["TemplateId"]) == UUID(params["TemplateId"]).hex

    assert fix_qid(expects={'interview_id': 'string'})(foo)(
        interview_id=params["TemplateId"]) == params["TemplateId"]

    with raises(ValueError):
        fix_qid(expects={'interview_id': 'error'})(foo)(
            interview_id=params["TemplateId"]) == params["TemplateId"]
