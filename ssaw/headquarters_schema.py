import sgqlc.types
import sgqlc.types.datetime


headquarters_schema = sgqlc.types.Schema()



########################################################################
# Scalars and Enumerations
########################################################################
class ApplyPolicy(sgqlc.types.Enum):
    __schema__ = headquarters_schema
    __choices__ = ('BEFORE_RESOLVER', 'AFTER_RESOLVER')


Boolean = sgqlc.types.Boolean

DateTime = sgqlc.types.datetime.DateTime

class Decimal(sgqlc.types.Scalar):
    __schema__ = headquarters_schema


Float = sgqlc.types.Float

ID = sgqlc.types.ID

Int = sgqlc.types.Int

class InterviewActionFlags(sgqlc.types.Enum):
    __schema__ = headquarters_schema
    __choices__ = ('CANBEREASSIGNED', 'CANBEDELETED', 'CANBEAPPROVED', 'CANBEUNAPPROVEDBYHQ', 'CANBEREJECTED', 'CANBERESTARTED', 'CANBEOPENED')


class InterviewStatus(sgqlc.types.Enum):
    __schema__ = headquarters_schema
    __choices__ = ('RESTORED', 'CREATED', 'SUPERVISORASSIGNED', 'INTERVIEWERASSIGNED', 'REJECTEDBYSUPERVISOR', 'READYFORINTERVIEW', 'SENTTOCAPI', 'RESTARTED', 'COMPLETED', 'APPROVEDBYSUPERVISOR', 'REJECTEDBYHEADQUARTERS', 'APPROVEDBYHEADQUARTERS', 'DELETED')


class Long(sgqlc.types.Scalar):
    __schema__ = headquarters_schema


class PaginationAmount(sgqlc.types.Scalar):
    __schema__ = headquarters_schema


class QuestionScope(sgqlc.types.Enum):
    __schema__ = headquarters_schema
    __choices__ = ('INTERVIEWER', 'SUPERVISOR', 'HEADQUARTER', 'HIDDEN')


class QuestionType(sgqlc.types.Enum):
    __schema__ = headquarters_schema
    __choices__ = ('SINGLEOPTION', 'MULTYOPTION', 'NUMERIC', 'DATETIME', 'GPSCOORDINATES', 'TEXT', 'TEXTLIST', 'QRBARCODE', 'MULTIMEDIA', 'AREA', 'AUDIO')


class SortOperationKind(sgqlc.types.Enum):
    __schema__ = headquarters_schema
    __choices__ = ('ASC', 'DESC')


String = sgqlc.types.String

class UserRoles(sgqlc.types.Enum):
    __schema__ = headquarters_schema
    __choices__ = ('ADMINISTRATOR', 'SUPERVISOR', 'INTERVIEWER', 'HEADQUARTER', 'OBSERVER', 'APIUSER')


class Uuid(sgqlc.types.Scalar):
    __schema__ = headquarters_schema



########################################################################
# Input Objects
########################################################################
class AssignmentsFilter(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('and_', 'archived', 'or_', 'questionnaire_id', 'received_by_tablet_at_utc', 'received_by_tablet_at_utc_gt', 'received_by_tablet_at_utc_lt', 'received_by_tablet_at_utc_not', 'responsible_id', 'responsible_id_in', 'responsible_id_not', 'responsible_id_not_in', 'web_mode')
    and_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('AssignmentsFilter')), graphql_name='AND')
    archived = sgqlc.types.Field(Boolean, graphql_name='archived')
    or_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('AssignmentsFilter')), graphql_name='OR')
    questionnaire_id = sgqlc.types.Field('QuestionnaireIdentity', graphql_name='questionnaireId')
    received_by_tablet_at_utc = sgqlc.types.Field(DateTime, graphql_name='receivedByTabletAtUtc')
    received_by_tablet_at_utc_gt = sgqlc.types.Field(DateTime, graphql_name='receivedByTabletAtUtc_gt')
    received_by_tablet_at_utc_lt = sgqlc.types.Field(DateTime, graphql_name='receivedByTabletAtUtc_lt')
    received_by_tablet_at_utc_not = sgqlc.types.Field(DateTime, graphql_name='receivedByTabletAtUtc_not')
    responsible_id = sgqlc.types.Field(Uuid, graphql_name='responsibleId')
    responsible_id_in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Uuid)), graphql_name='responsibleId_in')
    responsible_id_not = sgqlc.types.Field(Uuid, graphql_name='responsibleId_not')
    responsible_id_not_in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Uuid)), graphql_name='responsibleId_not_in')
    web_mode = sgqlc.types.Field(Boolean, graphql_name='webMode')


class InterviewFilter(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('and_', 'assignment_id', 'assignment_id_in', 'assignment_id_not', 'client_key', 'client_key_contains', 'client_key_in', 'client_key_starts_with', 'created_date_gt', 'created_date_gte', 'created_date_lt', 'created_date_lte', 'created_date_not_gt', 'created_date_not_gte', 'created_date_not_lt', 'created_date_not_lte', 'errors_count', 'errors_count_gt', 'identifying_questions_some', 'key', 'key_contains', 'key_in', 'key_starts_with', 'not_answered_count', 'not_answered_count_gt', 'not_answered_count_gte', 'not_answered_count_in', 'not_answered_count_lt', 'not_answered_count_lte', 'not_answered_count_not', 'not_answered_count_not_gt', 'not_answered_count_not_gte', 'not_answered_count_not_in', 'not_answered_count_not_lt', 'not_answered_count_not_lte', 'or_', 'questionnaire_id', 'questionnaire_variable', 'questionnaire_version', 'received_by_interviewer_at_utc', 'received_by_interviewer_at_utc_gt', 'received_by_interviewer_at_utc_lt', 'received_by_interviewer_at_utc_not', 'responsible_name', 'responsible_name_lower_case', 'responsible_name_lower_case_in', 'responsible_name_lower_case_starts_with', 'responsible_name_in', 'responsible_name_starts_with', 'responsible_role', 'status', 'status_in', 'status_not', 'supervisor_name', 'supervisor_name_lower_case', 'supervisor_name_lower_case_in', 'supervisor_name_lower_case_starts_with', 'supervisor_name_in', 'supervisor_name_starts_with', 'update_date_gt', 'update_date_gte', 'update_date_lt', 'update_date_lte', 'update_date_not_gt', 'update_date_not_gte', 'update_date_not_lt', 'update_date_not_lte')
    and_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('InterviewFilter')), graphql_name='AND')
    assignment_id = sgqlc.types.Field(Int, graphql_name='assignmentId')
    assignment_id_in = sgqlc.types.Field(sgqlc.types.list_of(Int), graphql_name='assignmentId_in')
    assignment_id_not = sgqlc.types.Field(Int, graphql_name='assignmentId_not')
    client_key = sgqlc.types.Field(String, graphql_name='clientKey')
    client_key_contains = sgqlc.types.Field(String, graphql_name='clientKey_contains')
    client_key_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='clientKey_in')
    client_key_starts_with = sgqlc.types.Field(String, graphql_name='clientKey_starts_with')
    created_date_gt = sgqlc.types.Field(DateTime, graphql_name='createdDate_gt')
    created_date_gte = sgqlc.types.Field(DateTime, graphql_name='createdDate_gte')
    created_date_lt = sgqlc.types.Field(DateTime, graphql_name='createdDate_lt')
    created_date_lte = sgqlc.types.Field(DateTime, graphql_name='createdDate_lte')
    created_date_not_gt = sgqlc.types.Field(DateTime, graphql_name='createdDate_not_gt')
    created_date_not_gte = sgqlc.types.Field(DateTime, graphql_name='createdDate_not_gte')
    created_date_not_lt = sgqlc.types.Field(DateTime, graphql_name='createdDate_not_lt')
    created_date_not_lte = sgqlc.types.Field(DateTime, graphql_name='createdDate_not_lte')
    errors_count = sgqlc.types.Field(Int, graphql_name='errorsCount')
    errors_count_gt = sgqlc.types.Field(Int, graphql_name='errorsCount_gt')
    identifying_questions_some = sgqlc.types.Field('QuestionAnswerFilter', graphql_name='identifyingQuestions_some')
    key = sgqlc.types.Field(String, graphql_name='key')
    key_contains = sgqlc.types.Field(String, graphql_name='key_contains')
    key_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='key_in')
    key_starts_with = sgqlc.types.Field(String, graphql_name='key_starts_with')
    not_answered_count = sgqlc.types.Field(Int, graphql_name='notAnsweredCount')
    not_answered_count_gt = sgqlc.types.Field(Int, graphql_name='notAnsweredCount_gt')
    not_answered_count_gte = sgqlc.types.Field(Int, graphql_name='notAnsweredCount_gte')
    not_answered_count_in = sgqlc.types.Field(sgqlc.types.list_of(Int), graphql_name='notAnsweredCount_in')
    not_answered_count_lt = sgqlc.types.Field(Int, graphql_name='notAnsweredCount_lt')
    not_answered_count_lte = sgqlc.types.Field(Int, graphql_name='notAnsweredCount_lte')
    not_answered_count_not = sgqlc.types.Field(Int, graphql_name='notAnsweredCount_not')
    not_answered_count_not_gt = sgqlc.types.Field(Int, graphql_name='notAnsweredCount_not_gt')
    not_answered_count_not_gte = sgqlc.types.Field(Int, graphql_name='notAnsweredCount_not_gte')
    not_answered_count_not_in = sgqlc.types.Field(sgqlc.types.list_of(Int), graphql_name='notAnsweredCount_not_in')
    not_answered_count_not_lt = sgqlc.types.Field(Int, graphql_name='notAnsweredCount_not_lt')
    not_answered_count_not_lte = sgqlc.types.Field(Int, graphql_name='notAnsweredCount_not_lte')
    or_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('InterviewFilter')), graphql_name='OR')
    questionnaire_id = sgqlc.types.Field(Uuid, graphql_name='questionnaireId')
    questionnaire_variable = sgqlc.types.Field(String, graphql_name='questionnaireVariable')
    questionnaire_version = sgqlc.types.Field(Long, graphql_name='questionnaireVersion')
    received_by_interviewer_at_utc = sgqlc.types.Field(DateTime, graphql_name='receivedByInterviewerAtUtc')
    received_by_interviewer_at_utc_gt = sgqlc.types.Field(DateTime, graphql_name='receivedByInterviewerAtUtc_gt')
    received_by_interviewer_at_utc_lt = sgqlc.types.Field(DateTime, graphql_name='receivedByInterviewerAtUtc_lt')
    received_by_interviewer_at_utc_not = sgqlc.types.Field(DateTime, graphql_name='receivedByInterviewerAtUtc_not')
    responsible_name = sgqlc.types.Field(String, graphql_name='responsibleName')
    responsible_name_lower_case = sgqlc.types.Field(String, graphql_name='responsibleNameLowerCase')
    responsible_name_lower_case_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='responsibleNameLowerCase_in')
    responsible_name_lower_case_starts_with = sgqlc.types.Field(String, graphql_name='responsibleNameLowerCase_starts_with')
    responsible_name_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='responsibleName_in')
    responsible_name_starts_with = sgqlc.types.Field(String, graphql_name='responsibleName_starts_with')
    responsible_role = sgqlc.types.Field(UserRoles, graphql_name='responsibleRole')
    status = sgqlc.types.Field(InterviewStatus, graphql_name='status')
    status_in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(InterviewStatus)), graphql_name='status_in')
    status_not = sgqlc.types.Field(InterviewStatus, graphql_name='status_not')
    supervisor_name = sgqlc.types.Field(String, graphql_name='supervisorName')
    supervisor_name_lower_case = sgqlc.types.Field(String, graphql_name='supervisorNameLowerCase')
    supervisor_name_lower_case_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='supervisorNameLowerCase_in')
    supervisor_name_lower_case_starts_with = sgqlc.types.Field(String, graphql_name='supervisorNameLowerCase_starts_with')
    supervisor_name_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='supervisorName_in')
    supervisor_name_starts_with = sgqlc.types.Field(String, graphql_name='supervisorName_starts_with')
    update_date_gt = sgqlc.types.Field(DateTime, graphql_name='updateDate_gt')
    update_date_gte = sgqlc.types.Field(DateTime, graphql_name='updateDate_gte')
    update_date_lt = sgqlc.types.Field(DateTime, graphql_name='updateDate_lt')
    update_date_lte = sgqlc.types.Field(DateTime, graphql_name='updateDate_lte')
    update_date_not_gt = sgqlc.types.Field(DateTime, graphql_name='updateDate_not_gt')
    update_date_not_gte = sgqlc.types.Field(DateTime, graphql_name='updateDate_not_gte')
    update_date_not_lt = sgqlc.types.Field(DateTime, graphql_name='updateDate_not_lt')
    update_date_not_lte = sgqlc.types.Field(DateTime, graphql_name='updateDate_not_lte')


class InterviewSort(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('assignment_id', 'created_date', 'errors_count', 'id', 'key', 'not_answered_count', 'questionnaire_id', 'questionnaire_version', 'received_by_interviewer_at_utc', 'responsible_name', 'responsible_role', 'status', 'update_date')
    assignment_id = sgqlc.types.Field(SortOperationKind, graphql_name='assignmentId')
    created_date = sgqlc.types.Field(SortOperationKind, graphql_name='createdDate')
    errors_count = sgqlc.types.Field(SortOperationKind, graphql_name='errorsCount')
    id = sgqlc.types.Field(SortOperationKind, graphql_name='id')
    key = sgqlc.types.Field(SortOperationKind, graphql_name='key')
    not_answered_count = sgqlc.types.Field(SortOperationKind, graphql_name='notAnsweredCount')
    questionnaire_id = sgqlc.types.Field(SortOperationKind, graphql_name='questionnaireId')
    questionnaire_version = sgqlc.types.Field(SortOperationKind, graphql_name='questionnaireVersion')
    received_by_interviewer_at_utc = sgqlc.types.Field(SortOperationKind, graphql_name='receivedByInterviewerAtUtc')
    responsible_name = sgqlc.types.Field(SortOperationKind, graphql_name='responsibleName')
    responsible_role = sgqlc.types.Field(SortOperationKind, graphql_name='responsibleRole')
    status = sgqlc.types.Field(SortOperationKind, graphql_name='status')
    update_date = sgqlc.types.Field(SortOperationKind, graphql_name='updateDate')


class MapsFilter(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('and_', 'file_name', 'file_name_in', 'file_name_starts_with', 'import_date_gt', 'import_date_gte', 'import_date_lt', 'import_date_lte', 'import_date_not_gt', 'import_date_not_gte', 'import_date_not_lt', 'import_date_not_lte', 'or_', 'size_gt', 'size_gte', 'size_lt', 'size_lte', 'size_not_gt', 'size_not_gte', 'size_not_lt', 'size_not_lte', 'users_some')
    and_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('MapsFilter')), graphql_name='AND')
    file_name = sgqlc.types.Field(String, graphql_name='fileName')
    file_name_in = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='fileName_in')
    file_name_starts_with = sgqlc.types.Field(String, graphql_name='fileName_starts_with')
    import_date_gt = sgqlc.types.Field(DateTime, graphql_name='importDate_gt')
    import_date_gte = sgqlc.types.Field(DateTime, graphql_name='importDate_gte')
    import_date_lt = sgqlc.types.Field(DateTime, graphql_name='importDate_lt')
    import_date_lte = sgqlc.types.Field(DateTime, graphql_name='importDate_lte')
    import_date_not_gt = sgqlc.types.Field(DateTime, graphql_name='importDate_not_gt')
    import_date_not_gte = sgqlc.types.Field(DateTime, graphql_name='importDate_not_gte')
    import_date_not_lt = sgqlc.types.Field(DateTime, graphql_name='importDate_not_lt')
    import_date_not_lte = sgqlc.types.Field(DateTime, graphql_name='importDate_not_lte')
    or_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('MapsFilter')), graphql_name='OR')
    size_gt = sgqlc.types.Field(Long, graphql_name='size_gt')
    size_gte = sgqlc.types.Field(Long, graphql_name='size_gte')
    size_lt = sgqlc.types.Field(Long, graphql_name='size_lt')
    size_lte = sgqlc.types.Field(Long, graphql_name='size_lte')
    size_not_gt = sgqlc.types.Field(Long, graphql_name='size_not_gt')
    size_not_gte = sgqlc.types.Field(Long, graphql_name='size_not_gte')
    size_not_lt = sgqlc.types.Field(Long, graphql_name='size_not_lt')
    size_not_lte = sgqlc.types.Field(Long, graphql_name='size_not_lte')
    users_some = sgqlc.types.Field('UserMapFilter', graphql_name='users_some')


class MapsSort(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('file_name', 'import_date', 'size')
    file_name = sgqlc.types.Field(SortOperationKind, graphql_name='fileName')
    import_date = sgqlc.types.Field(SortOperationKind, graphql_name='importDate')
    size = sgqlc.types.Field(SortOperationKind, graphql_name='size')


class QuestionAnswerFilter(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('and_', 'answer', 'answer_code', 'answer_code_in', 'answer_code_not', 'answer_code_not_in', 'answer_lower_case', 'answer_lower_case_not', 'answer_lower_case_not_starts_with', 'answer_lower_case_starts_with', 'answer_not', 'answer_not_starts_with', 'answer_starts_with', 'or_', 'question')
    and_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('QuestionAnswerFilter')), graphql_name='AND')
    answer = sgqlc.types.Field(String, graphql_name='answer')
    answer_code = sgqlc.types.Field(Decimal, graphql_name='answerCode')
    answer_code_in = sgqlc.types.Field(sgqlc.types.list_of(Decimal), graphql_name='answerCode_in')
    answer_code_not = sgqlc.types.Field(Decimal, graphql_name='answerCode_not')
    answer_code_not_in = sgqlc.types.Field(sgqlc.types.list_of(Decimal), graphql_name='answerCode_not_in')
    answer_lower_case = sgqlc.types.Field(String, graphql_name='answerLowerCase')
    answer_lower_case_not = sgqlc.types.Field(String, graphql_name='answerLowerCase_not')
    answer_lower_case_not_starts_with = sgqlc.types.Field(String, graphql_name='answerLowerCase_not_starts_with')
    answer_lower_case_starts_with = sgqlc.types.Field(String, graphql_name='answerLowerCase_starts_with')
    answer_not = sgqlc.types.Field(String, graphql_name='answer_not')
    answer_not_starts_with = sgqlc.types.Field(String, graphql_name='answer_not_starts_with')
    answer_starts_with = sgqlc.types.Field(String, graphql_name='answer_starts_with')
    or_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('QuestionAnswerFilter')), graphql_name='OR')
    question = sgqlc.types.Field('QuestionFilter', graphql_name='question')


class QuestionFilter(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('and_', 'identifying', 'or_', 'question_text', 'scope', 'variable')
    and_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('QuestionFilter')), graphql_name='AND')
    identifying = sgqlc.types.Field(Boolean, graphql_name='identifying')
    or_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('QuestionFilter')), graphql_name='OR')
    question_text = sgqlc.types.Field(String, graphql_name='questionText')
    scope = sgqlc.types.Field(QuestionScope, graphql_name='scope')
    variable = sgqlc.types.Field(String, graphql_name='variable')


class QuestionnaireIdentity(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('and_', 'id', 'id_not', 'or_', 'version', 'version_gt', 'version_gte', 'version_in', 'version_lt', 'version_lte', 'version_not', 'version_not_gt', 'version_not_gte', 'version_not_in', 'version_not_lt', 'version_not_lte')
    and_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('QuestionnaireIdentity')), graphql_name='AND')
    id = sgqlc.types.Field(Uuid, graphql_name='id')
    id_not = sgqlc.types.Field(Uuid, graphql_name='id_not')
    or_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('QuestionnaireIdentity')), graphql_name='OR')
    version = sgqlc.types.Field(Long, graphql_name='version')
    version_gt = sgqlc.types.Field(Long, graphql_name='version_gt')
    version_gte = sgqlc.types.Field(Long, graphql_name='version_gte')
    version_in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Long)), graphql_name='version_in')
    version_lt = sgqlc.types.Field(Long, graphql_name='version_lt')
    version_lte = sgqlc.types.Field(Long, graphql_name='version_lte')
    version_not = sgqlc.types.Field(Long, graphql_name='version_not')
    version_not_gt = sgqlc.types.Field(Long, graphql_name='version_not_gt')
    version_not_gte = sgqlc.types.Field(Long, graphql_name='version_not_gte')
    version_not_in = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Long)), graphql_name='version_not_in')
    version_not_lt = sgqlc.types.Field(Long, graphql_name='version_not_lt')
    version_not_lte = sgqlc.types.Field(Long, graphql_name='version_not_lte')


class UserMapFilter(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('and_', 'or_', 'user_name', 'user_name_not', 'user_name_not_starts_with', 'user_name_starts_with')
    and_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('UserMapFilter')), graphql_name='AND')
    or_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('UserMapFilter')), graphql_name='OR')
    user_name = sgqlc.types.Field(String, graphql_name='userName')
    user_name_not = sgqlc.types.Field(String, graphql_name='userName_not')
    user_name_not_starts_with = sgqlc.types.Field(String, graphql_name='userName_not_starts_with')
    user_name_starts_with = sgqlc.types.Field(String, graphql_name='userName_starts_with')



########################################################################
# Output Objects and Interfaces
########################################################################
class Assignment(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('archived', 'created_at_utc', 'email', 'id', 'interviews_needed', 'received_by_tablet_at_utc', 'responsible_id', 'web_mode')
    archived = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='archived')
    created_at_utc = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='createdAtUtc')
    email = sgqlc.types.Field(String, graphql_name='email')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    interviews_needed = sgqlc.types.Field(Int, graphql_name='interviewsNeeded')
    received_by_tablet_at_utc = sgqlc.types.Field(DateTime, graphql_name='receivedByTabletAtUtc')
    responsible_id = sgqlc.types.Field(sgqlc.types.non_null(Uuid), graphql_name='responsibleId')
    web_mode = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='webMode')


class CategoricalOption(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('parent_value', 'title', 'value')
    parent_value = sgqlc.types.Field(Int, graphql_name='parentValue')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    value = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='value')


class HeadquartersMutations(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('add_user_to_map', 'delete_map', 'delete_user_from_map')
    add_user_to_map = sgqlc.types.Field('Map', graphql_name='addUserToMap', args=sgqlc.types.ArgDict((
        ('file_name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='fileName', default=None)),
        ('user_name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='userName', default=None)),
))
    )
    delete_map = sgqlc.types.Field('Map', graphql_name='deleteMap', args=sgqlc.types.ArgDict((
        ('file_name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='fileName', default=None)),
))
    )
    delete_user_from_map = sgqlc.types.Field('Map', graphql_name='deleteUserFromMap', args=sgqlc.types.ArgDict((
        ('file_name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='fileName', default=None)),
        ('user_name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='userName', default=None)),
))
    )


class HeadquartersQuery(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('assignments', 'interviews', 'maps', 'questionnaires', 'questions', 'viewer')
    assignments = sgqlc.types.Field('IPagedConnectionOfAssignment', graphql_name='assignments', args=sgqlc.types.ArgDict((
        ('skip', sgqlc.types.Arg(Int, graphql_name='skip', default=None)),
        ('take', sgqlc.types.Arg(Int, graphql_name='take', default=None)),
        ('where', sgqlc.types.Arg(AssignmentsFilter, graphql_name='where', default=None)),
))
    )
    interviews = sgqlc.types.Field('IPagedConnectionOfInterview', graphql_name='interviews', args=sgqlc.types.ArgDict((
        ('order_by', sgqlc.types.Arg(InterviewSort, graphql_name='order_by', default=None)),
        ('skip', sgqlc.types.Arg(Int, graphql_name='skip', default=None)),
        ('take', sgqlc.types.Arg(Int, graphql_name='take', default=None)),
        ('where', sgqlc.types.Arg(InterviewFilter, graphql_name='where', default=None)),
))
    )
    maps = sgqlc.types.Field('IPagedConnectionOfMap', graphql_name='maps', args=sgqlc.types.ArgDict((
        ('order_by', sgqlc.types.Arg(MapsSort, graphql_name='order_by', default=None)),
        ('skip', sgqlc.types.Arg(Int, graphql_name='skip', default=None)),
        ('take', sgqlc.types.Arg(Int, graphql_name='take', default=None)),
        ('where', sgqlc.types.Arg(MapsFilter, graphql_name='where', default=None)),
))
    )
    questionnaires = sgqlc.types.Field('IPagedConnectionOfQuestionnaire', graphql_name='questionnaires', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(Uuid, graphql_name='id', default=None)),
        ('skip', sgqlc.types.Arg(Int, graphql_name='skip', default=None)),
        ('take', sgqlc.types.Arg(Int, graphql_name='take', default=None)),
        ('version', sgqlc.types.Arg(Long, graphql_name='version', default=None)),
))
    )
    questions = sgqlc.types.Field(sgqlc.types.list_of('Question'), graphql_name='questions', args=sgqlc.types.ArgDict((
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(Uuid), graphql_name='id', default=None)),
        ('language', sgqlc.types.Arg(String, graphql_name='language', default=None)),
        ('version', sgqlc.types.Arg(sgqlc.types.non_null(Long), graphql_name='version', default=None)),
        ('where', sgqlc.types.Arg(QuestionFilter, graphql_name='where', default=None)),
))
    )
    viewer = sgqlc.types.Field('User', graphql_name='viewer')


class IPagedConnectionOfAssignment(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('filtered_count', 'nodes', 'total_count')
    filtered_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='filteredCount')
    nodes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(Assignment)), graphql_name='nodes')
    total_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalCount')


class IPagedConnectionOfInterview(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('filtered_count', 'nodes', 'total_count')
    filtered_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='filteredCount')
    nodes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('Interview')), graphql_name='nodes')
    total_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalCount')


class IPagedConnectionOfMap(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('filtered_count', 'nodes', 'total_count')
    filtered_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='filteredCount')
    nodes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('Map')), graphql_name='nodes')
    total_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalCount')


class IPagedConnectionOfQuestionnaire(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('filtered_count', 'nodes', 'total_count')
    filtered_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='filteredCount')
    nodes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('Questionnaire')), graphql_name='nodes')
    total_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalCount')


class Interview(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('action_flags', 'assignment_id', 'client_key', 'created_date', 'errors_count', 'id', 'identifying_questions', 'key', 'not_answered_count', 'questionnaire_id', 'questionnaire_variable', 'questionnaire_version', 'received_by_interviewer', 'received_by_interviewer_at_utc', 'responsible_id', 'responsible_name', 'responsible_name_lower_case', 'responsible_role', 'status', 'supervisor_name', 'supervisor_name_lower_case', 'update_date', 'was_completed')
    action_flags = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(InterviewActionFlags))), graphql_name='actionFlags')
    assignment_id = sgqlc.types.Field(Int, graphql_name='assignmentId')
    client_key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='clientKey')
    created_date = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='createdDate')
    errors_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='errorsCount')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    identifying_questions = sgqlc.types.Field(sgqlc.types.list_of('QuestionAnswer'), graphql_name='identifyingQuestions')
    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='key')
    not_answered_count = sgqlc.types.Field(Int, graphql_name='notAnsweredCount')
    questionnaire_id = sgqlc.types.Field(sgqlc.types.non_null(Uuid), graphql_name='questionnaireId')
    questionnaire_variable = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='questionnaireVariable')
    questionnaire_version = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='questionnaireVersion')
    received_by_interviewer = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='receivedByInterviewer')
    received_by_interviewer_at_utc = sgqlc.types.Field(DateTime, graphql_name='receivedByInterviewerAtUtc')
    responsible_id = sgqlc.types.Field(sgqlc.types.non_null(Uuid), graphql_name='responsibleId')
    responsible_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='responsibleName')
    responsible_name_lower_case = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='responsibleNameLowerCase')
    responsible_role = sgqlc.types.Field(sgqlc.types.non_null(UserRoles), graphql_name='responsibleRole')
    status = sgqlc.types.Field(sgqlc.types.non_null(InterviewStatus), graphql_name='status')
    supervisor_name = sgqlc.types.Field(String, graphql_name='supervisorName')
    supervisor_name_lower_case = sgqlc.types.Field(String, graphql_name='supervisorNameLowerCase')
    update_date = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='updateDate')
    was_completed = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='wasCompleted')


class Map(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('file_name', 'import_date', 'max_scale', 'min_scale', 'size', 'users', 'wkid', 'x_max_val', 'x_min_val', 'y_max_val', 'y_min_val')
    file_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='fileName')
    import_date = sgqlc.types.Field(DateTime, graphql_name='importDate')
    max_scale = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='maxScale')
    min_scale = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='minScale')
    size = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='size')
    users = sgqlc.types.Field(sgqlc.types.list_of('UserMap'), graphql_name='users')
    wkid = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='wkid')
    x_max_val = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='xMaxVal')
    x_min_val = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='xMinVal')
    y_max_val = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='yMaxVal')
    y_min_val = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='yMinVal')


class Question(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('identifying', 'label', 'options', 'question_text', 'scope', 'type', 'variable')
    identifying = sgqlc.types.Field(Boolean, graphql_name='identifying')
    label = sgqlc.types.Field(String, graphql_name='label')
    options = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(CategoricalOption))), graphql_name='options')
    question_text = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='questionText')
    scope = sgqlc.types.Field(QuestionScope, graphql_name='scope')
    type = sgqlc.types.Field(sgqlc.types.non_null(QuestionType), graphql_name='type')
    variable = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='variable')


class QuestionAnswer(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('answer', 'answer_lower_case', 'answer_value', 'question')
    answer = sgqlc.types.Field(String, graphql_name='answer')
    answer_lower_case = sgqlc.types.Field(String, graphql_name='answerLowerCase')
    answer_value = sgqlc.types.Field(Int, graphql_name='answerValue')
    question = sgqlc.types.Field(sgqlc.types.non_null(Question), graphql_name='question')


class Questionnaire(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('default_language_name', 'id', 'questionnaire_id', 'title', 'translations', 'variable', 'version')
    default_language_name = sgqlc.types.Field(String, graphql_name='defaultLanguageName')
    id = sgqlc.types.Field(ID, graphql_name='id')
    questionnaire_id = sgqlc.types.Field(sgqlc.types.non_null(Uuid), graphql_name='questionnaireId')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    translations = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Translation'))), graphql_name='translations')
    variable = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='variable')
    version = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='version')


class Translation(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('id', 'name')
    id = sgqlc.types.Field(sgqlc.types.non_null(Uuid), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')


class User(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('id', 'roles', 'user_name')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    roles = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(UserRoles))), graphql_name='roles')
    user_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='userName')


class UserMap(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('user_name',)
    user_name = sgqlc.types.Field(String, graphql_name='userName')



########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
headquarters_schema.query_type = HeadquartersQuery
headquarters_schema.mutation_type = HeadquartersMutations
headquarters_schema.subscription_type = None

