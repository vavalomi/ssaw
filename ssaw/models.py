import re
import sys
from datetime import datetime
from enum import Enum, IntEnum
from typing import Dict, List, Optional, Tuple, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, Extra, Field, validator

from .headquarters_schema import Map
from .utils import get_properties, parse_date, to_hex, to_pascal

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


class InterviewParaAction(Enum):
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
    INTERVIEW_MODE_CHANGED = 'InterviewModeChanged'
    KEY_ASSIGNED = 'KeyAssigned'
    ANSWER_SET = 'AnswerSet'
    QUESTION_DECLARED_VALID = 'QuestionDeclaredValid'
    RECIEVED_BY_SUPERVISOR = 'ReceivedBySupervisor'

    @property
    def code(self):
        return self.value.ordinal()


class InterviewHistoryAction(IntEnum):
    SupervisorAssigned = 0
    InterviewerAssigned = 1
    AnswerSet = 2
    AnswerRemoved = 3
    CommentSet = 4
    Completed = 5
    Restarted = 6
    ApproveBySupervisor = 7
    ApproveByHeadquarter = 8
    RejectedBySupervisor = 9
    RejectedByHeadquarter = 10
    Deleted = 11
    Restored = 12
    QuestionEnabled = 13
    QuestionDisabled = 14
    GroupEnabled = 15
    GroupDisabled = 16
    QuestionDeclaredValid = 17
    QuestionDeclaredInvalid = 18
    UnapproveByHeadquarters = 19
    ReceivedByInterviewer = 20
    ReceivedBySupervisor = 21
    VariableSet = 22
    VariableEnabled = 23
    VariableDisabled = 24
    Paused = 25
    Resumed = 26
    KeyAssigned = 27
    TranslationSwitched = 28
    OpenedBySupervisor = 29
    ClosedBySupervisor = 30
    InterviewModeChanged = 31
    InterviewCreated = 32


class InterviewAction(IntEnum):
    SupervisorAssigned = 0
    InterviewerAssigned = 1
    FirstAnswerSet = 2
    Completed = 3
    Restarted = 4
    ApprovedBySupervisor = 5
    ApprovedByHeadquarter = 6
    RejectedBySupervisor = 7
    RejectedByHeadquarter = 8
    Deleted = 9
    Restored = 10
    UnapprovedByHeadquarter = 11
    InterviewCreated = 12
    InterviewReceivedByTablet = 13
    Resumed = 14
    Paused = 15
    TranslationSwitched = 16
    OpenedBySupervisor = 17
    ClosedBySupervisor = 18
    InterviewSwitchedToCawiMode = 19
    InterviewSwitchedToCapiMode = 20


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
            id_ = to_hex(ans["QuestionId"]["Id"])
            variable_name = ans["VariableName"]
            if variable_name not in self._variables:
                self._variables[variable_name] = Question(variable_name=variable_name, public_key=id_)
                self._public_ids[id_] = variable_name
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
                elif self._variables[t[0]].yes_no_view:
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

    def _get_variable(self, variable: Optional[str] = None, question_id: Optional[str] = None):
        if variable:
            if variable not in self._variables:
                raise TypeError("variable not found")
        elif question_id:
            variable = self._public_ids.get(to_hex(question_id))
        else:
            raise TypeError(
                "either 'variable' or 'question_id' argument is required")
        return variable


class BaseModelWithConfig(BaseModel):
    class Config:
        alias_generator = to_pascal
        allow_population_by_field_name = True
        extra = Extra.allow


class AssignmentHistoryItemAdditionalData(BaseModelWithConfig):
    comment: Optional[str] = ""
    responsible: Optional[str]
    new_responsible: Optional[str]
    upgraded_from_id: Optional[int]


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
    utc_date: datetime
    additional_data: Optional[AssignmentHistoryItemAdditionalData]

    def to_datarow(self):
        return {
            "assignment__id": None,
            "date": self.utc_date.strftime("%Y-%m-%d"),
            "time": self.utc_date.strftime("%H:%M:%S"),
            "action": ASSIGNMENT_ACTION_TYPES[self.action],
            "originator": self.actor_name,
            "role": "",
            "responsible__name":
                (self.additional_data.responsible or self.additional_data.new_responsible)
                if self.additional_data else "",
            "responsible__role": "",
            "old__value": "",
            "new__value": "",
            "comment": self.additional_data.comment if self.additional_data else "",
        }


class InterviewHistoryItemParameter(BaseModelWithConfig):
    question: Optional[str]
    answer: Optional[str]
    roster: Optional[List[int]]
    comment: Optional[str]
    mode: Optional[str]
    responsible: Optional[str]
    key: Optional[str]

    @validator('roster', pre=True)
    def split_str(cls, v):
        return v.split(',') if v and isinstance(v, str) else []


class InteriviewHistoryItem(BaseModelWithConfig):
    index: int
    action: str
    originator_name: Optional[str]
    originator_role: Optional[str]
    parameters: Optional[InterviewHistoryItemParameter]
    timestamp: datetime


class ValidationCondition(BaseModelWithConfig):
    expression: str
    message: str
    severity: int = 0


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


JSON_TYPE_FIELD_NAME = "$type"


class Variable(BaseModelWithConfig):
    obj_type: Literal["Variable"] = Field(alias=JSON_TYPE_FIELD_NAME)
    public_key: UUID = Field(default_factory=uuid4)
    name: str
    label: str = ""
    type: VariableType
    expression: str
    do_not_export: bool = False
    variable_name: str


class Category(BaseModelWithConfig):
    id: UUID
    name: str


class LookupTable(BaseModelWithConfig):
    table_name: str
    file_name: str


class StaticText(BaseModelWithConfig):
    obj_type: Literal["StaticText"] = Field(alias=JSON_TYPE_FIELD_NAME)
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
    condition_expression: Optional[str]
    featured: bool = False
    hide_if_disabled: bool = False
    instructions: Optional[str]
    properties: Optional[QuestionProperties]
    public_key: UUID = Field(default_factory=uuid4)
    parent_id: Optional[UUID]
    question_scope: QuestionScope = QuestionScope.INTERVIEWER
    question_text: Optional[str]
    question_type: QuestionType = QuestionType.TEXT
    stata_export_caption: Optional[str]
    validation_conditions: List[ValidationCondition] = []
    variable_label: Optional[str]
    variable_name: str


class TextQuestion(Question):
    obj_type: Literal["TextQuestion"] = Field(alias=JSON_TYPE_FIELD_NAME)
    mask: Optional[str]
    value: Optional[str]


class NumericQuestion(Question):
    obj_type: Literal["NumericQuestion"] = Field(alias=JSON_TYPE_FIELD_NAME,
                                                 default="NumericQuestion",
                                                 const=True)
    is_integer: bool = False
    value: Optional[float]

    def __gt__(self, num):
        return self.value > num

    def __lt__(self, num):
        return self.value < num


class Answer(BaseModelWithConfig):
    answer_text: str
    answer_value: int


class SingleQuestion(Question):
    obj_type: Literal["SingleQuestion"] = Field(alias=JSON_TYPE_FIELD_NAME,
                                                default="SingleQuestion",
                                                const=True)
    answers: List[Answer] = []
    cascade_from_question_id: Optional[UUID]
    categories_id: Optional[UUID]
    is_filtered_combobox: bool = False
    show_as_list: bool = False
    linked_to_question_id: Optional[UUID]
    linked_to_roster_id: Optional[UUID]


class MultiOptionsQuestion(Question):
    obj_type: Literal["MultyOptionsQuestion"] = Field(alias=JSON_TYPE_FIELD_NAME,
                                                      default="MultyOptionsQuestion",
                                                      const=True)
    answers: List[Answer] = []
    are_answers_ordered: bool = False
    yes_no_view: bool = False
    linked_to_question_id: Optional[UUID]
    linked_to_roster_id: Optional[UUID]


class DateTimeQuestion(Question):
    obj_type: Literal["DateTimeQuestion"] = Field(alias=JSON_TYPE_FIELD_NAME)
    is_timestamp: bool = False


class TextListQuestion(Question):
    obj_type: Literal["TextListQuestion"] = Field(alias=JSON_TYPE_FIELD_NAME)
    max_answer_count: int


class GpsCoordinateQuestion(Question):
    obj_type: Literal["GpsCoordinateQuestion"] = Field(alias=JSON_TYPE_FIELD_NAME,
                                                       default="GpsCoordinateQuestion",
                                                       const=True)
    question_type: Literal[6]


class QRBarcodeQuestion(Question):
    obj_type: Literal["QRBarcodeQuestion"] = Field(alias=JSON_TYPE_FIELD_NAME,
                                                   default="QRBarcodeQuestion",
                                                   const=True)


class MultimediaQuestion(Question):
    obj_type: Literal["MultimediaQuestion"] = Field(alias=JSON_TYPE_FIELD_NAME,
                                                    default="MultimediaQuestion",
                                                    const=True)


class AudioQuestion(Question):
    obj_type: Literal["AudioQuestion"] = Field(alias=JSON_TYPE_FIELD_NAME,
                                               default="AudioQuestion",
                                               const=True)


class AreaQuestion(Question):
    obj_type: Literal["AreaQuestion"] = Field(alias=JSON_TYPE_FIELD_NAME,
                                              default="AreaQuestion",
                                              const=True)


class RosterSource(Enum):
    FIXED = 1
    OTHER = 0


class Group(BaseModelWithConfig):
    obj_type: Literal["Group"] = Field(alias=JSON_TYPE_FIELD_NAME)
    description: str = ""
    display_mode: int = 0
    fixed_roster_titles: list = []
    is_flat_mode: bool = False
    is_plain_mode: bool = False
    is_roster: bool = False
    public_key: UUID = Field(default_factory=uuid4)
    parent_id: Optional[UUID]
    roster_size_source: RosterSource = RosterSource.FIXED
    roster_size_question_id: Optional[UUID]
    roster_title_question_id: Optional[UUID]
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
    creation_date: datetime
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
    time: datetime


class User(BaseModelWithConfig):
    user_name: str
    password: str
    role: UserRole = UserRole.INTERVIEWER
    supervisor: Optional[str]
    full_name: Optional[str]
    email: Optional[str]
    phone_number: Optional[str]


class Version():
    def __init__(self, version_string: str):
        pattern = r"(\d{1,2})\.(\d{1,2})(\.\d+)? \(build (\d+)\)"
        m = re.match(pattern, version_string, flags=re.IGNORECASE)
        if m:
            self.major = int(m.group(1))
            self.minor = int(m.group(2))
            self.patch = int(m.group(3)[1:]) if m.group(3) else 0
            self.build = int(m.group(4))
            self.version_string = version_string
        else:
            # dev version
            pattern = r"(\d{1,2})\.(\d{1,2})\.(\d+)\.(\d+)"
            m = re.match(pattern, version_string, flags=re.IGNORECASE)
            if m:
                self.major = int(m.group(1))
                self.minor = int(m.group(2))
                self.patch = int(m.group(3))
                self.build = int(m.group(4))
                self.version_string = version_string
            else:
                # somehow malformed version string, assume most recent
                self.version_string = version_string
                self.build = sys.maxsize

    def __repr__(self):
        return self.version_string

    def __lt__(self, other: "Version"):
        if self.major != other.major:
            return self.major < other.major

        if self.minor != other.minor:
            return self.minor < other.minor

        if self.patch != other.patch:
            return self.patch < other.patch
        else:
            return self.build < other.build

    def __eq__(self, other: "Version"):
        return self.build == other.build


class Assignment(BaseModelWithConfig):
    responsible: str
    quantity: int
    questionnaire_id: str
    identifying_data: Optional[List[dict]]
    email: Optional[str]
    password: Optional[str]
    web_mode: Optional[bool] = False
    is_audio_recording_enabled: Optional[bool] = False
    comments: Optional[str]
    protected_variables: Optional[List[str]]


class AssignmentResult(Assignment):
    id: int
    responsible_id: UUID
    responsible: str = Field(alias="ResponsibleName")
    interviews_count: int
    archived: bool
    created_at_utc: datetime
    updated_at_utc: Optional[datetime]
    received_by_tablet_at_utc: Optional[datetime]


class AssignmentList(BaseModelWithConfig):
    order: Optional[str]
    limit: int
    total_count: int
    offset: int
    assignments: List[AssignmentResult]


class AssignmentWebLink(BaseModelWithConfig):
    link: str = Field(alias="assignment__link")
    id: int = Field(alias="assignment__id")
    email: Optional[str] = Field(alias="assignment__email")
    password: Optional[str] = Field(alias="assignment__password")


class ExportJobLinks(BaseModelWithConfig):
    cancel: Optional[str]
    download: Optional[str]


class ExportJob(BaseModelWithConfig):
    export_type: Optional[Literal["Tabular", "STATA", "SPSS", "Binary", "DDI", "Paradata"]] = "Tabular"
    questionnaire_id: str
    interview_status: Optional[Literal["All", "SupervisorAssigned", "InterviewerAssigned",
                                       "RejectedBySupervisor", "Completed", "ApprovedBySupervisor",
                                       "RejectedByHeadquarters", "ApprovedByHeadquarters"]] = "All"
    from_date: Optional[datetime] = Field(alias="From")
    to_date: Optional[datetime] = Field(alias="To")
    access_token: Optional[str]
    refresh_token: Optional[str]
    storage_type: Optional[Literal["Dropbox", "OneDrive", "GoogleDrive"]]
    translation_id: Optional[UUID]
    include_meta: Optional[bool]


class ExportJobResult(ExportJob):
    job_id: int
    export_status: Literal["Created", "Running", "Completed", "Fail", "Canceled"]
    start_date: datetime
    complete_date: Optional[datetime]
    progress: int
    eta: Optional[str] = Field(alias="ETA")
    error: Optional[str]
    links: ExportJobLinks
    has_export_file: bool

    @validator("start_date", "complete_date", "from_date", "to_date", pre=True, check_fields=False)
    def time_validate(cls, v):
        return parse_date(v)


class Workspace(BaseModelWithConfig):
    name: str
    display_name: str
    disabled_at_utc: Optional[datetime]


class WorkspacesList(BaseModelWithConfig):
    order: Optional[str]
    limit: int
    total_count: int
    offset: int
    workspaces: List[Workspace]


class WorkspaceStatus(BaseModelWithConfig):
    can_be_deleted: bool
    workspace_name: str
    workspace_display_name: str
    existing_questionnaires_count: int
    interviewers_count: int
    supervisors_count: int
    maps_count: int


QuestionnaireIdentity = Union[str, Tuple[str, int]]
