import datetime
import re
import sys
from enum import Enum
from typing import Dict, List, Optional, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Extra, Field

from .headquarters_schema import Map
from .utils import get_properties, parse_date, to_camel, to_hex, to_qidentity

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


class QuestionScope(Enum):
    INTERVIEWER = 0
    SUPERVISOR = 1
    HIDDEN = 3


class UserRole(Enum):
    ADMINISTRATOR = "Administrator"
    SUPERVISOR = "Supervisor"
    INTERVIEWER = "Interviewer"
    HEADQUARTERS = "Headquarter"
    OBSERVER = "Observer"
    APIUSER = "ApiUser"

    @property
    def code(self):
        if self.name == "ADMINISTRATOR":
            return 4
        elif self.name == "SUPERVISOR":
            return 2
        elif self.name == "INTERVIEWER":
            return 1
        elif self.name == "HEADQUARTERS":
            return 3
        elif self.name == "APIUSER":
            return 5
        else:
            return 0


class InterviewAction(Enum):
    SUPERVISOR_ASSIGNED = "SupervisorAssigned"
    INTERVIEWER_ASSIGNED = "InterviewerAssigned"
    FIRST_ANSWER_SET = "FirstAnswerSet"
    COMPLETED = "Completed"
    RESTARTED = "Restarted"
    APPROVED_BY_SUPERVISOR = "ApprovedBySupervisor"
    APPROVED_BY_HEADQUARTERS = "ApprovedByHeadquarter"
    REJECTED_BY_SUPERVISOR = "RejectedBySupervisor"
    REJECTED_BY_HEADQUARTERS = "RejectedByHeadquarter"
    DELETED = "Deleted"
    RESTORED = "Restored"
    UNAPPROVED_BY_HEADQUARTERS = "UnapprovedByHeadquarter"
    CREATED = "Created"
    INTERVIEW_RECEIVED_BY_TABLET = "InterviewReceivedByTablet"
    RESUMED = "Resumed"
    PAUSED = "Paused"
    TRANSLATION_SWITCHED = "TranslationSwitched"
    OPENED_BY_SUPERVISOR = "OpenedBySupervisor"
    CLOSED_BY_SUPERVISOR = "ClosedBySupervisor"

    @property
    def code(self):
        return self.value.ordinal()


class Assignment(object):
    def __init__(self, responsible: str, quantity: int, questionnaire_id,
                 identifying_data=None, email: str = "", password: str = "", webmode: bool = False,
                 audio_recording_enabled: bool = False, comments: str = "", protected_variables: list = None):
        """An assignment.

            :param responsible: responsible username
            :param quantity: [description]
            :param questionnaire_id: [description]
            :param email: [description], defaults to ""
            :param password: [description], defaults to ""
            :param webmode: [description], defaults to False
            :param audio_recording_enabled: [description], defaults to False
            :param comments: [description], defaults to ""
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
        self.protected_variables = protected_variables

    def __str__(self):
        return(str(self.__dict__))

    @classmethod
    def from_dict(cls, dict):
        obj = cls(
            responsible=dict["ResponsibleName"],
            quantity=dict["Quantity"],
            questionnaire_id=dict["QuestionnaireId"],
            identifying_data=dict["IdentifyingData"] if "IdentifyingData" in dict else [
            ],
            email=dict["Email"],
            password=dict["Password"],
            webmode=dict["WebMode"]
        )
        setattr(obj, "id", dict["Id"])
        setattr(obj, "responsible_id", dict["ResponsibleId"])
        setattr(obj, "interviews_count", dict["InterviewsCount"])
        setattr(obj, "archived", dict["Archived"])
        setattr(obj, "created_utc", dict["CreatedAtUtc"])
        setattr(obj, "updated_utc", dict["UpdatedAtUtc"])
        if "IsAudioRecordingEnabled" in dict:
            setattr(obj, "audio_recording_enabled",
                    dict["IsAudioRecordingEnabled"])
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
            "ProtectedVariables": self.protected_variables
        }


class ExportJob(object):
    def __init__(self,
                 questionnaire_identity: str,
                 export_type="Tabular",
                 interview_status="All",
                 from_date=None,
                 to_date=None,
                 access_token: str = None,
                 storage_type: str = None):
        """ExportJob object.

        :param questionnaire_identity: [description]
        :param export_type: [description], default to "Tabular"
        :param interview_status: [description], defaults to "All"
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
            export_type=dict["ExportType"],
            questionnaire_identity=dict["QuestionnaireId"],
            interview_status=dict["InterviewStatus"],
            from_date=dict["From"] if "From" in dict else None,
            to_date=dict["To"] if "To" in dict else None,
            access_token=dict["AccessToken"] if "AccessToken" in dict else None,
            storage_type=dict["StorageType"] if "StorageType" in dict else None
        )
        setattr(obj, "job_id", dict["JobId"])
        setattr(obj, "_export_status", dict["ExportStatus"])
        setattr(obj, "start_date", parse_date(dict["StartDate"]))
        setattr(obj, "complete_date", parse_date(dict["CompleteDate"]))
        setattr(obj, "progress", dict["Progress"])
        if "ETA" in dict:
            setattr(obj, "eta", dict["ETA"])
        if "Links" in dict:
            if "Cancel" in dict["Links"]:
                setattr(obj, "_cancel_link", dict["Links"]["Cancel"])
            if "Download" in dict["Links"]:
                setattr(obj, "_download_link", dict["Links"]["Download"])
        setattr(obj, "_has_export_file", dict["HasExportFile"])
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
        self._public_ids = {}
        self._groups = {}
        self._data = {}
        self._raw_data = []
        if questionnaire_document:
            self._variables = get_properties(questionnaire_document)
            self._public_ids = {var.public_key.hex: variable_name for variable_name, var in self._variables.items()}
            self._groups = get_properties(questionnaire_document, groups=True, items=False)

    def __iter__(self):
        return iter(self._raw_data)

    def __str__(self) -> str:
        return(str(self._raw_data))

    def from_dict(self, answers: list):

        self._raw_data = answers
        for ans in self._raw_data:
            val = ans["Answer"]
            if val is None:
                continue
            id = to_hex(ans["QuestionId"]["Id"])
            variable_name = ans["VariableName"]
            if variable_name not in self._variables:
                self._variables[variable_name] = Question(variable_name=variable_name, public_key=id)
                self._public_ids[id] = variable_name
            key = (variable_name, ) + tuple(ans["QuestionId"]["RosterVector"])
            self._data[key] = val

    def dict(self, prefilling: bool = True) -> list:
        ret = []
        for t, answer in self._data.items():
            identity = self._variables[t[0]].public_key.hex
            if len(t) > 1:
                identity += "_" + "-".join(str(r) for r in t[1:])

            ans = answer
            q_type = self._variables[t[0]].question_type

            if q_type == QuestionType.LIST:
                ans_split = answer if type(answer) == list else answer.split("|")
                if prefilling:
                    ans = str(ans_split)
                else:
                    ans = [
                        {
                            "value": i + 1,
                            "isProtected": False,
                            "text": ans_split[i],
                        }
                        for i in range(len(ans_split))
                    ]

            elif q_type == QuestionType.MULTI_SELECT:
                ans_split = answer if type(answer) == list else answer.split(",")
                if prefilling:
                    ans = str(ans_split)
                else:
                    if self._variables[t[0]].yes_no_view:
                        ans = ans = [{"value": i, "isProtected": False, "yes": (i in ans_split)}
                                     for i in range(1, len(self._variables[t[0]].answers) + 1)]
                    else:
                        ans = ans_split

            elif q_type == QuestionType.SINGLE_SELECT and self._variables[t[0]].linked_to_roster_id and not prefilling:
                if type(ans) != list:
                    ans = [answer, ]
            ret.append({"Identity": identity, "Answer": ans})

        return ret

    def answer_variables(self) -> list:
        return [t[0] for t in self._data]

    def get_answer(self, variable: str = None, question_id: str = None, roster_vector: list = None):
        key = self._get_key(variable=variable, question_id=question_id, roster_vector=roster_vector)
        return self._data.get(key)

    def set_answer(self, answer, variable: str = None, question_id: str = None, roster_vector: list = []):
        key = self._get_key(variable=variable, question_id=question_id, roster_vector=roster_vector)
        variable = self._get_variable(variable=variable, question_id=question_id)
        self._data[key] = answer

    def remove_answer(self, variable: str = None, question_id: str = None, roster_vector: list = None):
        key = self._get_key(variable=variable, question_id=question_id, roster_vector=roster_vector)
        if key in self._data:
            del self._data[key]

    def needed_preloading(self) -> set:
        needed = set()
        for variable in self._data:
            triggers = self._find_roster_trigger(variable[0])
            if triggers:
                needed.update(triggers)
        return needed

    def _find_roster_trigger(self, variable) -> set:
        ret = set()
        parent_obj = self._groups.get(self._variables[variable].parent_id)
        if parent_obj.is_roster:
            trigger_id = parent_obj.roster_size_question_id.hex
            trigger_var = self._public_ids[trigger_id]
            if (trigger_var, ) not in self._data:
                ret.add(trigger_var)
            ret_in = self._find_roster_trigger(trigger_var)
            if ret_in:
                ret.update(ret_in)

        return ret

    def _get_key(self, roster_vector: list = [], **kwargs):
        key = (self._get_variable(**kwargs), )
        if roster_vector:
            key += tuple(roster_vector) if type(roster_vector) == list else tuple([roster_vector, ])
        return key

    def _get_variable(self, variable: str = None, question_id: str = None):
        if variable:
            if variable not in self._variables:
                raise TypeError("variable not found")
        else:
            if question_id:
                variable = self._public_ids.get(to_hex(question_id))
            else:
                raise TypeError(
                    "either 'variable' or 'question_id' argument is required")
        return variable


class BaseModelWithConfig(BaseModel):
    class Config:
        alias_generator = to_camel
        allow_population_by_field_name = True
        extra = Extra.allow


class AssignmentHistoryItemAdditionalData(BaseModelWithConfig):
    comment: str
    responsible: str = Field(alias="NewResponsible")


ASSIGNMENT_ACTION_TYPES = {
    "Unknown": 0,
    "Created": 1,
    "Archived": 2,
    "Deleted": 3,
    "ReceivedByTablet": 4,
    "UnArchived": 5,
    "AudioRecordingChanged": 6,
    "Reassigned": 7,
    "QuantityChanged": 8,
    "WebModeChanged": 9
}


class AssignmentHistoryItem(BaseModelWithConfig):
    action: str
    actor_name: str
    utc_date: datetime.datetime
    additional_data: AssignmentHistoryItemAdditionalData

    def to_datarow(self):
        return {
            "assignment__id": None,
            "date": self.utc_date.strftime("%Y-%m-%d"),
            "time": self.utc_date.strftime("%H:%M:%S"),
            "action": ASSIGNMENT_ACTION_TYPES[self.action],
            "originator": self.actor_name,
            "role": "",
            "responsible__name": self.additional_data.responsible,
            "responsible__role": "",
            "old__value": "",
            "new__value": "",
            "comment": self.additional_data.comment
        }


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
    obj_type: Literal["Variable"] = Field(alias="$type")
    public_key: UUID = Field(default_factory=uuid4)
    name: str
    label: str = ""
    type: VariableType
    expression: str
    do_not_export: bool
    variable_name: str


class Category(BaseModelWithConfig):
    id: UUID
    name: str


class LookupTable(BaseModelWithConfig):
    table_name: str
    file_name: str


class StaticText(BaseModelWithConfig):
    obj_type: Literal["StaticText"] = Field(alias="$type")
    public_key: UUID = Field(default_factory=uuid4)
    text: str
    attachment_name: str = ""
    hide_if_disabled: bool = False
    validation_conditions: List[ValidationCondition] = []
    variable_name: str


class QuestionProperties(BaseModelWithConfig):
    hide_instructions: bool = False
    use_formatting: bool = False


class Question(BaseModelWithConfig):
    condition_expression: str = ""
    featured: bool = False
    hide_if_disabled: bool = False
    instructions: str = ""
    properties: QuestionProperties = None
    public_key: UUID = Field(default_factory=uuid4)
    parent_id: UUID = None
    question_scope: QuestionScope = QuestionScope.INTERVIEWER
    question_text: str = ""
    question_type: QuestionType = QuestionType.TEXT
    stata_export_caption: str = ""
    validation_conditions: List[ValidationCondition] = []
    variable_label: Optional[str] = ""
    variable_name: str


class TextQuestion(Question):
    obj_type: Literal["TextQuestion"] = Field(alias="$type")
    mask: str = None
    value: str = ""


class NumericQuestion(Question):
    obj_type: Literal["NumericQuestion"] = Field(alias="$type",
                                                 default="NumericQuestion",
                                                 const="NumericQuestion")
    is_integer: bool = False
    value: float = None

    def __gt__(self, num):
        return self.value > num

    def __lt__(self, num):
        return self.value < num


class Answer(BaseModelWithConfig):
    answer_text: str
    answer_value: int


class SingleQuestion(Question):
    obj_type: Literal["SingleQuestion"] = Field(alias="$type",
                                                default="SingleQuestion",
                                                const="SingleQuestion")
    answers: List[Answer] = []
    cascade_from_question_id: UUID = None
    categories_id: UUID = None
    is_filtered_combobox: bool = False
    show_as_list: bool = False
    linked_to_question_id: UUID = None
    linked_to_roster_id: UUID = None


class MultiOptionsQuestion(Question):
    obj_type: Literal["MultyOptionsQuestion"] = Field(alias="$type",
                                                      default="MultyOptionsQuestion",
                                                      const="MultyOptionsQuestion")
    answers: List[Answer] = []
    are_answers_ordered: bool = False
    yes_no_view: bool = False
    linked_to_question_id: UUID = None
    linked_to_roster_id: UUID = None


class DateTimeQuestion(Question):
    obj_type: Literal["DateTimeQuestion"] = Field(alias="$type")
    is_timestamp: bool


class TextListQuestion(Question):
    obj_type: Literal["TextListQuestion"] = Field(alias="$type")
    max_answer_count: int


class GpsCoordinateQuestion(Question):
    obj_type: Literal["GpsCoordinateQuestion"] = Field(alias="$type",
                                                       default="GpsCoordinateQuestion",
                                                       const="GpsCoordinateQuestion")
    question_type: Literal[6]


class QRBarcodeQuestion(Question):
    obj_type: Literal["QRBarcodeQuestion"] = Field(alias="$type",
                                                   default="QRBarcodeQuestion",
                                                   const="QRBarcodeQuestion")


class MultimediaQuestion(Question):
    obj_type: Literal["MultimediaQuestion"] = Field(alias="$type",
                                                    default="MultimediaQuestion",
                                                    const="MultimediaQuestion")


class AudioQuestion(Question):
    obj_type: Literal["AudioQuestion"] = Field(alias="$type",
                                               default="AudioQuestion",
                                               const="AudioQuestion")


class AreaQuestion(Question):
    obj_type: Literal["AreaQuestion"] = Field(alias="$type",
                                              default="AreaQuestion",
                                              const="AreaQuestion")


class RosterSource(Enum):
    FIXED = 1
    OTHER = 0


class Group(BaseModelWithConfig):
    obj_type: Literal["Group"] = Field(alias="$type")
    description: str = ""
    display_mode: int = 0
    fixed_roster_titles: list = []
    is_flat_mode: bool = False
    is_plain_mode: bool = False
    is_roster: bool = False
    public_key: UUID = Field(default_factory=uuid4)
    parent_id: UUID = None
    roster_size_source: RosterSource = RosterSource.FIXED
    roster_size_question_id: UUID = None
    roster_title_question_id: UUID = None
    title: str
    variable_name: str
    children: List[Union[StaticText, NumericQuestion, TextQuestion, TextListQuestion,
                         SingleQuestion, MultiOptionsQuestion, DateTimeQuestion,
                         Variable, AreaQuestion, AudioQuestion, GpsCoordinateQuestion,
                         MultimediaQuestion, QRBarcodeQuestion, "Group"]] = []


class Attachment(BaseModelWithConfig):
    attachment_id: UUID
    content_id: str
    name: str


class QuestionnaireDocument(BaseModelWithConfig):
    attachments: List[Attachment]
    categories: List[Category]
    children: List[Group]
    creation_date: datetime.datetime
    lookup_tables: Dict[UUID, LookupTable]
    macros: Dict[UUID, Macro]
    public_key: UUID = Field(default_factory=uuid4)
    title: str
    translations: list
    variable_name: str

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        def attach_parent_id(obj):
            if hasattr(obj, "children"):
                for ch in obj.children:
                    ch.parent_id = obj.public_key.hex
                    attach_parent_id(ch)

        attach_parent_id(self)


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
            # dev version
            pattern = r"(\d{1,2})\.(\d{1,2})\.(\d+)\.(\d+)"
            m = re.match(pattern, version_string, flags=re.IGNORECASE)
            if m:
                self.major = int(m.group(1))
                self.minor = int(m.group(2))
                self.patch = int(m.group(3))
                self.build = int(m.group(4))
                self.version = version_string
            else:
                # somehow malformed version string, assume most recent
                self.version = version_string
                self.build = sys.maxsize

    def __repr__(self):
        return self.version

    def __lt__(self, other: "Version"):
        return self.build < other.build

    def __eq__(self, other: "Version"):
        return self.build == other.build


class AssignmentWebLink(BaseModelWithConfig):
    link: str = Field(alias="assignment__link")
    id: int = Field(alias="assignment__id")
    email: Optional[str] = Field(alias="assignment__email")
    password: Optional[str] = Field(alias="assignment__password")
