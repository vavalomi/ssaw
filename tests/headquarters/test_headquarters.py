import json
from uuid import UUID

from pytest import raises

from ssaw import AssignmentsApi, Client, MapsApi, QuestionnairesApi, headquarters_schema as schema
from ssaw.exceptions import GraphQLError, IncompleteQuestionnaireIdError, UnauthorizedError
from ssaw.models import Group, QuestionnaireDocument
from ssaw.utils import filter_object, fix_qid, get_properties, order_object, parse_qidentity


from . import my_vcr


@my_vcr.use_cassette()
def test_headquarters_unathorized():
    s = Client('https://demo.mysurvey.solutions/', "aa", "")

    with raises(UnauthorizedError):  # graphql endpoint
        next(QuestionnairesApi(s).get_list())

    with raises(UnauthorizedError):  # rest endpoint
        next(AssignmentsApi(s).get_list())


@my_vcr.use_cassette()
def test_headquarters_graphql_error(session):

    with raises(GraphQLError):
        next(MapsApi(session, workspace="dddd").get_list())


def test_headquarters_user_session_login(session, params):
    with raises(UnauthorizedError):
        QuestionnairesApi(session).download_web_links(params['TemplateId'], params['TemplateVersion'])


def test_utils_parse_qidentity():

    random_guid = "f6a5bd80-fdb4-40b6-8759-0f7531c4a3df"
    qidentity = f"{random_guid}$1"
    a = parse_qidentity(qidentity)
    assert a == qidentity.replace("-", ""), "UUID in hex format $ version"

    with raises(IncompleteQuestionnaireIdError):
        parse_qidentity(random_guid)

    a = parse_qidentity((random_guid, 1))
    assert a == "{}${}".format(UUID(random_guid).hex, 1)


def test_utils_fix_qid():

    random_guid = "f6a5bd80-fdb4-40b6-8759-0f7531c4a3df"

    def foo(interview_id):
        return interview_id

    assert fix_qid(expects={'interview_id': 'hex'})(foo)(
        interview_id=random_guid) == UUID(random_guid).hex

    assert fix_qid(expects={'interview_id': 'string'})(foo)(
        interview_id=random_guid) == random_guid

    with raises(ValueError):
        fix_qid(expects={'interview_id': 'error'})(foo)(interview_id=random_guid)

    with raises(ValueError):
        fix_qid(expects={'interview_id': 'string'})(foo)(interview_id="random string")


def test_utils_order_object():
    # params as list of field names
    obj = order_object(classname="MapsSort", params=["file_name"])
    assert isinstance(obj[0], schema.MapsSort), "result must be a list of MapsSort objects"
    assert obj[0].file_name == "ASC"

    # params as tuple of field names
    obj = order_object(classname="MapsSort", params=("file_name", "size"))
    assert obj[0].file_name == "ASC"
    assert obj[1].size == "ASC"

    # params as tuple of tuples
    obj = order_object(classname="MapsSort", params=(("file_name", "DESC"),))
    assert obj[0].file_name == "DESC"

    # mix of field name and tuples
    obj = order_object(classname="MapsSort", params=("size", ("file_name", "DESC")))
    assert obj[0].size == "ASC"
    assert obj[1].file_name == "DESC"

    # params as dictionary
    obj = order_object(classname="MapsSort", params={"size": "ASC", "file_name": "DESC"})
    assert obj[0].size == "ASC"
    assert obj[1].file_name == "DESC"

    # must be one of list, tuple or dict
    with raises(TypeError):
        _ = order_object(classname="MapsSort", params="size")

    # element must be string or tuple
    with raises(TypeError):
        _ = order_object(classname="MapsSort", params=["size", 4])


def test_utils_filter_object():
    obj = filter_object(classname="InterviewsFilter", not_answered_count=3)
    assert isinstance(obj, schema.InterviewsFilter)
    assert obj.not_answered_count.eq == 3

    # two parameters
    obj = filter_object(classname="InterviewsFilter", not_answered_count=3, key="aaa")
    assert obj.key.eq == "aaa"

    # only where, just return what received
    where = schema.InterviewsFilter(key=schema.StringOperationFilterInput(eq="aaa"))
    obj = filter_object(classname="InterviewsFilter", where=where)
    assert obj == where

    # mixing keyword and where params
    obj = filter_object(classname="InterviewsFilter", not_answered_count=3,
                        where=schema.InterviewsFilter(key=schema.StringOperationFilterInput(eq="aaa")))
    assert obj.and_[0].key.eq == "aaa"
    assert obj.and_[1].not_answered_count.eq == 3

    # always search user names in case-insensitive (lower) form
    obj = filter_object(classname="InterviewsFilter", responsible_name="AAA")
    assert obj.responsible_name.eq == "aaa"

    # non-existant filter field
    with raises(KeyError):
        _ = filter_object(classname="InterviewsFilter", something="something")

    # wrong type of the where parameter
    with raises(TypeError):
        _ = filter_object(classname="InterviewsFilter", where="something")


def test_get_properties():
    questionnaire_document = """
{
  "CoverPageSectionId": "c46ee895-0e6e-4063-8136-31e6bfa7c3f8",
  "Id": "3659b4f36cef41569c5d36b694a08c64",
  "Revision": 0,
  "Children": [
    {
      "$type": "Group",
      "Children": [
        {
          "$type": "TextQuestion",
          "Answers": [],
          "Children": [],
          "ConditionExpression": "",
          "HideIfDisabled": false,
          "Featured": false,
          "Properties": {
            "HideInstructions": false,
            "UseFormatting": false,
            "OptionsFilterExpression": ""
          },
          "PublicKey": "96e15d81-329f-3eae-605e-56d9b550804d",
          "QuestionScope": 0,
          "QuestionText": "Where is your property located?",
          "QuestionType": 7,
          "StataExportCaption": "address",
          "IsTimestamp": false,
          "ValidationConditions": [],
          "VariableName": "address"
        },
        {
          "$type": "NumericQuestion",
          "IsInteger": true,
          "UseFormatting": false,
          "AnswerOrder": 2,
          "Answers": [],
          "Children": [],
          "ConditionExpression": "",
          "HideIfDisabled": false,
          "Featured": false,
          "Properties": {
            "HideInstructions": false,
            "UseFormatting": false,
            "OptionsFilterExpression": ""
          },
          "PublicKey": "8a81acd7-445e-7772-ac30-620110c34131",
          "QuestionScope": 0,
          "QuestionText": "How many rooms do you have?",
          "QuestionType": 4,
          "StataExportCaption": "nrooms",
          "IsTimestamp": false,
          "ValidationConditions": [
            {
              "Expression": "self < 10",
              "Message": "Are you sure you have more than 10 rooms?",
              "Severity": 0
            }
          ],
          "VariableName": "nrooms"
        },
        {
          "$type": "SingleQuestion",
          "ShowAsList": false,
          "Answers": [
            {
              "AnswerText": "apartment in a multi-family building",
              "AnswerValue": "1"
            },
            {
              "AnswerText": "single-family dwelling",
              "AnswerValue": "2"
            },
            {
              "AnswerText": "hotel",
              "AnswerValue": "3"
            }
          ],
          "Children": [],
          "ConditionExpression": "",
          "HideIfDisabled": false,
          "Featured": false,
          "Properties": {
            "HideInstructions": false,
            "UseFormatting": false,
            "OptionsFilterExpression": ""
          },
          "PublicKey": "eb0c9210-41e0-aa9d-d248-43ec843f69b5",
          "QuestionScope": 0,
          "QuestionText": "What type of the dwelling it is?",
          "QuestionType": 0,
          "StataExportCaption": "apttype",
          "LinkedFilterExpression": "",
          "IsFilteredCombobox": false,
          "IsTimestamp": false,
          "ValidationConditions": [],
          "VariableName": "apttype"
        },
        {
          "$type": "GpsCoordinateQuestion",
          "AnswerOrder": 2,
          "Answers": [],
          "Children": [],
          "ConditionExpression": "",
          "HideIfDisabled": false,
          "Featured": false,
          "Properties": {
            "HideInstructions": false,
            "UseFormatting": false,
            "OptionsFilterExpression": ""
          },
          "PublicKey": "5a8485be-779e-455f-b8c9-f89598911abc",
          "QuestionScope": 0,
          "QuestionText": "Please collect gps location of the property",
          "QuestionType": 6,
          "StataExportCaption": "location",
          "IsTimestamp": false,
          "ValidationConditions": [],
          "VariableName": "location"
        },
        {
          "$type": "MultimediaQuestion",
          "QuestionType": 11,
          "IsSignature": false,
          "AnswerOrder": 2,
          "Answers": [],
          "Children": [],
          "ConditionExpression": "",
          "HideIfDisabled": false,
          "Featured": false,
          "Properties": {
            "HideInstructions": false,
            "UseFormatting": false,
            "OptionsFilterExpression": ""
          },
          "PublicKey": "3c934512-5117-9431-f0d2-dbce213374ef",
          "QuestionScope": 0,
          "QuestionText": "Please take a picture of the exterior entrance",
          "StataExportCaption": "exterior",
          "IsTimestamp": false,
          "ValidationConditions": [],
          "VariableName": "exterior"
        },
        {
          "$type": "Group",
          "Children": [
            {
              "$type": "TextQuestion",
              "Answers": [],
              "Children": [],
              "ConditionExpression": "",
              "HideIfDisabled": false,
              "Featured": false,
              "Properties": {
                "HideInstructions": false,
                "UseFormatting": false,
                "OptionsFilterExpression": ""
              },
              "PublicKey": "d3e0bb30-dcf7-5035-2f8a-bf7778ebd6b3",
              "QuestionScope": 0,
              "QuestionText": "bla bal",
              "QuestionType": 7,
              "StataExportCaption": "some",
              "IsTimestamp": false,
              "ValidationConditions": [],
              "VariableName": "some"
            }
          ],
          "ConditionExpression": "",
          "HideIfDisabled": false,
          "IsFlatMode": false,
          "IsPlainMode": false,
          "DisplayMode": 0,
          "Enabled": true,
          "Description": "",
          "VariableName": "",
          "IsRoster": false,
          "CustomRosterTitle": false,
          "RosterSizeSource": 0,
          "FixedRosterTitles": [],
          "PublicKey": "dabe8801-b748-75d4-8dc8-af942946fcf7",
          "Title": "describe neighborhood"
        },
        {
          "$type": "Group",
          "Children": [
            {
              "$type": "SingleQuestion",
              "ShowAsList": false,
              "Answers": [
                {
                  "AnswerText": "bedroom",
                  "AnswerValue": "1"
                },
                {
                  "AnswerText": "living room",
                  "AnswerValue": "2"
                },
                {
                  "AnswerText": "storage",
                  "AnswerValue": "3"
                },
                {
                  "AnswerText": "kitchen",
                  "AnswerValue": "4"
                }
              ],
              "Children": [],
              "ConditionExpression": "",
              "HideIfDisabled": false,
              "Featured": false,
              "Properties": {
                "HideInstructions": false,
                "UseFormatting": false,
                "OptionsFilterExpression": ""
              },
              "PublicKey": "c200738a-1323-212a-0905-d632903d5b29",
              "QuestionScope": 0,
              "QuestionText": "What is the type of this room?",
              "QuestionType": 0,
              "StataExportCaption": "roomtype",
              "LinkedFilterExpression": "",
              "IsFilteredCombobox": false,
              "IsTimestamp": false,
              "ValidationConditions": [],
              "VariableName": "roomtype"
            },
            {
              "$type": "NumericQuestion",
              "IsInteger": true,
              "UseFormatting": false,
              "AnswerOrder": 2,
              "Answers": [],
              "Children": [],
              "ConditionExpression": "",
              "HideIfDisabled": false,
              "Featured": false,
              "Properties": {
                "HideInstructions": false,
                "UseFormatting": false,
                "OptionsFilterExpression": ""
              },
              "PublicKey": "8cc7c8c5-a516-7a5c-a3bd-bca8297848d8",
              "QuestionScope": 0,
              "QuestionText": "What is the room area (m2)",
              "QuestionType": 4,
              "StataExportCaption": "area",
              "IsTimestamp": false,
              "ValidationConditions": [],
              "VariableName": "area"
            }
          ],
          "ConditionExpression": "apttype < 3",
          "HideIfDisabled": true,
          "IsFlatMode": false,
          "IsPlainMode": false,
          "DisplayMode": 0,
          "Enabled": true,
          "Description": "",
          "VariableName": "rooms",
          "IsRoster": true,
          "CustomRosterTitle": false,
          "RosterSizeQuestionId": "8a81acd7-445e-7772-ac30-620110c34131",
          "RosterSizeSource": 0,
          "FixedRosterTitles": [],
          "PublicKey": "a5eaec2a-8d4a-1bc6-39bc-07dca9011b1a",
          "Title": "New roster"
        },
        {
          "$type": "AreaQuestion",
          "AnswerOrder": 2,
          "Answers": [],
          "Children": [],
          "ConditionExpression": "",
          "HideIfDisabled": false,
          "Featured": false,
          "Properties": {
            "HideInstructions": false,
            "UseFormatting": false,
            "OptionsFilterExpression": "",
            "GeometryType": 0
          },
          "PublicKey": "a40144df-53ae-122a-0bfa-356c3e6c2c81",
          "QuestionScope": 0,
          "QuestionText": "geo",
          "QuestionType": 12,
          "StataExportCaption": "geo",
          "IsTimestamp": false,
          "ValidationConditions": [],
          "VariableName": "geo"
        }
      ],
      "ConditionExpression": "",
      "HideIfDisabled": false,
      "IsFlatMode": false,
      "IsPlainMode": false,
      "DisplayMode": 0,
      "Enabled": true,
      "Description": "",
      "VariableName": "",
      "IsRoster": false,
      "CustomRosterTitle": false,
      "RosterSizeSource": 0,
      "FixedRosterTitles": [],
      "PublicKey": "168d5a57-a370-4602-8153-ac2bb5418f7d",
      "Title": "Dwelling info"
    }
  ],
  "Macros": {},
  "LookupTables": {},
  "Attachments": [],
  "Translations": [
    {
      "Id": "178af991-6455-883a-ca0d-e7edfbe718fc",
      "Name": "ქართული"
    }
  ],
  "Categories": [],
  "ConditionExpression": "",
  "HideIfDisabled": false,
  "CreationDate": "2019-04-08T21:42:23.6019877",
  "LastEntryDate": "2021-05-14T19:29:03.5935433",
  "IsDeleted": false,
  "CreatedBy": "5339442c-c634-42c4-950b-914e02bcc7fe",
  "IsPublic": false,
  "PublicKey": "381144e5-1b21-41fa-8601-7c319a833ec1",
  "Title": "Prueba",
  "Description": "",
  "VariableName": "prueba",
  "IsRoster": false,
  "DisplayMode": 0,
  "RosterSizeSource": 0,
  "FixedRosterTitles": [],
  "LastEventSequence": 0,
  "IsUsingExpressionStorage": false,
  "CustomRosterTitle": false,
  "IsCoverPageSupported": false
}
    """
    Group.update_forward_refs()
    q = QuestionnaireDocument(**json.loads(questionnaire_document))

    vars_only = set(get_properties(q, groups=False).keys())
    all = set(get_properties(q, groups=True).keys())
    groups_only = set(get_properties(q, groups=True, items=False).keys())

    assert all - vars_only == groups_only, "groups and items filters must add up to all"

    gps_questions = get_properties(q, types="GpsCoordinateQuestion")
    assert list(gps_questions.keys()) == ["location"], "single gps question must be found"

    vars_with_properties = get_properties(q, types="NumericQuestion", properties=["question_text", "featured"])
    assert vars_with_properties["nrooms"] == {"featured": False, "question_text": "How many rooms do you have?"}
