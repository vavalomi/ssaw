import datetime
import re
import sys
from enum import Enum
from typing import Dict, List, Union
from uuid import UUID

from pydantic import BaseModel, Extra, Field

from .headquarters_schema import Map
from .utils import get_variables, to_camel, to_hex, to_qidentity

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


__all__ = ["Assignment", "ExportJob", "Map", ]


class QuestionType(Enum):
    SINGLE_SELECT = 0
    MULTI_SELECT = 3
    NUMERIC = 4
    DATE = 5
    GPS = 6
    TEXT = 7
    LIST = 9
    BARCODE = 10
    PICTURE = 11
    GEOGRAPHY = 12
    AUDIO = 13


class QuestionTypeLiteral(Enum):
    SINGLE_SELECT = "SingleQuestion"
    MULTI_SELECT = "MultyOptionsQuestion"
    NUMERIC = "NumericQuestion"
    DATE = "DateTimeQuestion"
    GPS = "GpsCoordinateQuestion"
    TEXT = "TextQuestion"
    LIST = "TextListQuestion"
    BARCODE = "QRBarcodeQuestion"
    PICTURE = "MultimediaQuestion"
    GEOGRAPHY = "AreaQuestion"
    AUDIO = "AudioQuestion"


class UserRole(Enum):
    ADMINISTRATOR = "Administrator"
    SUPERVISOR = "Supervisor"
    INTERVIEWER = "Interviewer"
    HEADQUARTERS = "Headquarter"
    OBSERVER = "Observer"
    APIUSER = "ApiUser"


class Assignment(object):
    def __init__(self, responsible: str, quantity: int, questionnaire_id,
                 identifying_data=None, email: str = '', password: str = '', webmode: bool = False,
                 audio_recording_enabled: bool = False, comments: str = ''):
        """An assignment.

            :param responsible: responsible username
            :param quantity: [description]
            :param questionnaire_id: [description]
            :param email: [description], defaults to ''
            :param password: [description], defaults to ''
            :param webmode: [description], defaults to False
            :param audio_recording_enabled: [description], defaults to False
            :param comments: [description], defaults to ''
        """

        self.responsible = responsible
        self.quantity = quantity
        self.questionnaire_id = questionnaire_id
        self.identifying_data = identifying_data
        self.email = email
        self.password = password
        self.webmode = webmode
        self.audio_recording_enabled = audio_recording_enabled
        self.comments = comments

    def __str__(self):
        return(str(self.__dict__))

    @classmethod
    def from_dict(cls, dict):
        obj = cls(
            responsible=dict['ResponsibleName'],
            quantity=dict['Quantity'],
            questionnaire_id=dict['QuestionnaireId'],
            identifying_data=dict['IdentifyingData'] if 'IdentifyingData' in dict else [
            ],
            email=dict['Email'],
            password=dict['Password'],
            webmode=dict['WebMode']
        )
        setattr(obj, 'id', dict['Id'])
        setattr(obj, 'responsible_id', dict['ResponsibleId'])
        setattr(obj, 'interviews_count', dict['InterviewsCount'])
        setattr(obj, 'archived', dict['Archived'])
        setattr(obj, 'created_utc', dict['CreatedAtUtc'])
        setattr(obj, 'updated_utc', dict['UpdatedAtUtc'])
        if 'IsAudioRecordingEnabled' in dict:
            setattr(obj, 'audio_recording_enabled',
                    dict['IsAudioRecordingEnabled'])
        return obj

    def to_json(self):
        return {
            "Responsible": self.responsible,
            "Quantity": self.quantity,
            "QuestionnaireId": self.questionnaire_id,
            "Email": self.email,
            "Password": self.password,
            "WebMode": self.webmode,
            "IsAudioRecordingEnabled": self.audio_recording_enabled,
            "Comments": self.comments,
            "IdentifyingData": self.identifying_data,
        }


class ExportJob(object):
    def __init__(self,
                 questionnaire_identity: str,
                 export_type='Tabular',
                 interview_status='All',
                 from_date=None,
                 to_date=None,
                 access_token: str = None,
                 storage_type: str = None):
        """ExportJob object.

        :param questionnaire_identity: [description]
        :param export_type: [description], default to 'Tabular'
        :param interview_status: [description], defaults to 'All'
        :param from_date: [description], defaults to None
        :param to_date: [description], defaults to None
        :param access_token: [description], defaults to None
        :param storage_type: [description], defaults to None
        """

        if type(questionnaire_identity) is tuple:
            (questionnaire_id, questionnaire_version) = questionnaire_identity
            questionnaire_identity = to_qidentity(
                questionnaire_id, questionnaire_version)

        self.questionnaire_identity = questionnaire_identity
        self.export_type = export_type
        self.interview_status = interview_status
        self.from_date = from_date
        self.to_date = to_date
        self.access_token = access_token
        self.storage_type = storage_type
        self._export_status: str
        self._has_export_file: bool
        self._cancel_link: str
        self._download_link: str

    @property
    def export_status(self) -> str:
        return self._export_status

    @property
    def has_export_file(self) -> bool:
        return self._has_export_file

    @property
    def cancel_link(self) -> str:
        return self._cancel_link

    @property
    def download_link(self) -> str:
        return self._download_link

    def __str__(self) -> str:
        return(str(self.__dict__))

    @classmethod
    def from_dict(cls, dict):
        obj = cls(
            export_type=dict['ExportType'],
            questionnaire_identity=dict['QuestionnaireId'],
            interview_status=dict['InterviewStatus'],
            from_date=dict['From'] if 'From' in dict else None,
            to_date=dict['To'] if 'To' in dict else None,
            access_token=dict['AccessToken'] if 'AccessToken' in dict else None,
            storage_type=dict['StorageType'] if 'StorageType' in dict else None
        )
        setattr(obj, 'job_id', dict['JobId'])
        setattr(obj, '_export_status', dict['ExportStatus'])
        setattr(obj, 'start_date', dict['StartDate'])
        setattr(obj, 'complete_date', dict['CompleteDate'])
        setattr(obj, 'progress', dict['Progress'])
        if 'ETA' in dict:
            setattr(obj, 'eta', dict['ETA'])
        if 'Links' in dict:
            if 'Cancel' in dict['Links']:
                setattr(obj, '_cancel_link', dict['Links']['Cancel'])
            if 'Download' in dict['Links']:
                setattr(obj, '_download_link', dict['Links']['Download'])
        setattr(obj, '_has_export_file', dict['HasExportFile'])
        return obj

    def to_json(self):
        ret = {
            "ExportType": self.export_type,
            "QuestionnaireId": self.questionnaire_identity,
            "InterviewStatus": self.interview_status,
            "From": self.from_date,
            "To": self.to_date,
            "AccessToken": self.access_token,
            "StorageType": self.storage_type,
        }
        return {k: v for k, v in ret.items() if v is not None}


class InterviewAnswers(object):
    def __init__(self, questionnaire_document=None):
        self._variables = {}
        self._data = {}
        self._raw_data = []
        if questionnaire_document:
            types = [
                QuestionTypeLiteral.BARCODE.value,
                QuestionTypeLiteral.SINGLE_SELECT.value,
                QuestionTypeLiteral.MULTI_SELECT.value,
                QuestionTypeLiteral.DATE.value,
                QuestionTypeLiteral.GPS.value,
                QuestionTypeLiteral.LIST.value,
                QuestionTypeLiteral.NUMERIC.value,
                QuestionTypeLiteral.TEXT.value
            ]
            for var in get_variables(questionnaire_document, types):
                if getattr(var, "linked_to_question_id", None) is not None:
                    continue  # preloading is not allowed for categorical linked questions
                self._variables[var.variable_name] = var.public_key.hex

    def __iter__(self):
        return iter(self._raw_data)

    def __str__(self) -> str:
        return(str(self._raw_data))

    @classmethod
    def from_dict(cls, answers: list):
        obj = cls()
        obj._raw_data = answers
        for ans in obj._raw_data:
            val = ans["Answer"]
            if val is None:
                continue
            id = to_hex(ans["QuestionId"]["Id"])
            obj._variables[ans["VariableName"]] = id
            if len(ans["QuestionId"]["RosterVector"]) > 0:
                key = id + "_" + "-".join([str(r) for r in ans["QuestionId"]["RosterVector"]])
            else:
                key = id
            obj._data[key] = val
        return(obj)

    def dict(self) -> dict:
        return([{"Identity": k, "Answer": v} for k, v in self._data.items()])

    def get_answer(self, variable: str = None, question_id: str = None, roster_vector: list = None):
        key = self._get_key(variable=variable, question_id=question_id, roster_vector=roster_vector)
        if key in self._data:
            return self._data[key]

    def set_answer(self, answer, variable: str = None, question_id: str = None, roster_vector: list = []):
        key = self._get_key(variable=variable, question_id=question_id, roster_vector=roster_vector)
        self._data[key] = answer

    def _get_key(self, variable: str = None, question_id: str = None, roster_vector: list = []):
        if variable:
            if variable in self._variables:
                key = self._variables[variable]
            else:
                raise TypeError("variable not found")
        else:
            if question_id:
                key = to_hex(question_id)
            else:
                raise TypeError(
                    "either 'variable' or 'question_id' argument is required")

        if roster_vector is not None:
            if type(roster_vector) is not list:
                roster_vector = [roster_vector]
            key = key + "_" + "-".join([str(r) for r in roster_vector])

        return(key)


class BaseModelWithConfig(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
        extra = Extra.allow


class ValidationCondition(BaseModelWithConfig):
    expression: str
    message: str
    severity: int


class Macro(BaseModelWithConfig):
    name: str
    content: str
    description: str = ""


class VariableType(Enum):
    BOOLEAN = 3
    DOUBLE = 2
    DATE = 4
    LONG = 1
    STRING = 5


class Variable(BaseModelWithConfig):
    obj_type: Literal['Variable'] = Field(alias="$type")
    public_key: UUID
    name: str
    label: str = ""
    type: VariableType
    expression: str
    do_not_export: bool
    variable_name: str


class Category(BaseModelWithConfig):
    id: UUID
    name: str


class StaticText(BaseModelWithConfig):
    obj_type: Literal['StaticText'] = Field(alias="$type")
    public_key: UUID
    text: str
    attachment_name: str = ""
    hide_if_disabled: bool
    validation_conditions: List[ValidationCondition] = []
    variable_name: str


class QuestionProperties(BaseModelWithConfig):
    hide_instructions: bool = False
    use_formatting: bool = False


class Question(BaseModelWithConfig):
    condition_expression: str
    featured: bool
    hide_if_disabled: bool
    instructions: str = ""
    properties: QuestionProperties = None
    public_key: UUID
    question_scope: int
    question_text: str
    Question_type: QuestionType
    stata_export_caption: str
    validation_conditions = []
    variable_name: str


class TextQuestion(Question):
    obj_type: Literal['TextQuestion'] = Field(alias="$type")
    mask: str = None


class NumericQuestion(Question):
    obj_type: Literal['NumericQuestion'] = Field(alias="$type")
    is_integer: bool


class Answer(BaseModelWithConfig):
    answer_text: str
    answer_value: int


class SingleQuestion(Question):
    obj_type: Literal['SingleQuestion'] = Field(alias="$type")
    answers: List[Answer]
    cascade_from_question_id: UUID = None
    categories_id: UUID = None
    is_filtered_combobox: bool
    show_as_list: bool
    linked_to_question_id: UUID = None


class MultyOptionsQuestion(Question):
    obj_type: Literal['MultyOptionsQuestion'] = Field(alias="$type")
    answers: List[Answer]
    are_answers_ordered: bool
    yes_no_view: bool
    linked_to_question_id: UUID = None


class DateTimeQuestion(Question):
    obj_type: Literal['DateTimeQuestion'] = Field(alias="$type")
    is_timestamp: bool


class TextListQuestion(Question):
    obj_type: Literal['TextListQuestion'] = Field(alias="$type")
    max_answer_count: int


class GpsCoordinateQuestion(Question):
    obj_type: Literal[QuestionTypeLiteral.GPS.value] = Field(alias="$type")


class QRBarcodeQuestion(Question):
    obj_type: Literal[QuestionTypeLiteral.BARCODE.value] = Field(alias="$type")


class MultimediaQuestion(Question):
    obj_type: Literal[QuestionTypeLiteral.PICTURE.value] = Field(alias="$type")


class AudioQuestion(Question):
    obj_type: Literal[QuestionTypeLiteral.AUDIO.value] = Field(alias="$type")


class AreaQuestion(Question):
    obj_type: Literal[QuestionTypeLiteral.GEOGRAPHY.value] = Field(alias="$type")


class RosterSource(Enum):
    FIXED = 1
    OTHER = 0


class Group(BaseModelWithConfig):
    obj_type: Literal['Group'] = Field(alias="$type")
    children: List[Union[StaticText, NumericQuestion, TextQuestion,
                         SingleQuestion, MultyOptionsQuestion, DateTimeQuestion, Variable, "Group"]]
    description: str = ""
    display_mode: int
    fixed_roster_titles: list
    is_flat_mode: bool
    is_plain_mode: bool
    is_roster: bool
    public_key: UUID
    roster_size_source: RosterSource
    roster_size_question_id: UUID = None
    roster_title_question_id: UUID = None
    title: str
    variable_name: str


class Attachment(BaseModelWithConfig):
    attachment_id: UUID
    content_id: str
    name: str


class QuestionnaireDocument(BaseModelWithConfig):
    attachments: List[Attachment]
    categories: List[Category]
    children: List[Group]
    creation_date: datetime.datetime
    cover_page_section_id: UUID = None
    lookup_tables: dict
    macros: Dict[UUID, Macro]
    public_key: UUID
    title: str
    translations: list
    variable_name: str


class InterviewerAction(BaseModelWithConfig):
    message: str
    time: datetime.datetime


class User(BaseModelWithConfig):
    user_name: str
    password: str
    role: UserRole = UserRole.INTERVIEWER
    supervisor: str = None
    full_name: str = None
    email: str = None
    phone_number: str = None


class Version():
    def __init__(self, version_string: str):
        pattern = r"(\d{1,2})\.(\d{1,2})(\.\d+)? \(build (\d+)\)"
        m = re.match(pattern, version_string, flags=re.IGNORECASE)
        if m:
            self.major = int(m.group(1))
            self.minor = int(m.group(2))
            self.patch = int(m.group(3)[1:]) if m.group(3) else 0
            self.build = int(m.group(4))
            self.version = version_string
        else:
            # assume dev version, therefore most recent
            self.version = version_string
            self.build = sys.maxsize

    def __repr__(self):
        return self.version

    def __lt__(self, other: "Version"):
        return self.build < other.build

    def __eq__(self, other: "Version"):
        return self.build == other.build
