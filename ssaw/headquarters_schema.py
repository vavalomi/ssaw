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


class EntityType(sgqlc.types.Enum):
    __schema__ = headquarters_schema
    __choices__ = ('SECTION', 'QUESTION', 'STATICTEXT', 'VARIABLE', 'ROSTER')


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


class QuestionScope(sgqlc.types.Enum):
    __schema__ = headquarters_schema
    __choices__ = ('INTERVIEWER', 'SUPERVISOR', 'HEADQUARTER', 'HIDDEN')


class QuestionType(sgqlc.types.Enum):
    __schema__ = headquarters_schema
    __choices__ = ('SINGLEOPTION', 'MULTYOPTION', 'NUMERIC', 'DATETIME', 'GPSCOORDINATES', 'TEXT', 'TEXTLIST', 'QRBARCODE', 'MULTIMEDIA', 'AREA', 'AUDIO')


class SortEnumType(sgqlc.types.Enum):
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
    __field_names__ = ('and_', 'or_', 'id', 'questionnaire_id', 'archived', 'responsible_id', 'web_mode', 'received_by_tablet_at_utc')
    and_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('AssignmentsFilter')), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('AssignmentsFilter')), graphql_name='or')
    id = sgqlc.types.Field('ComparableInt32OperationFilterInput', graphql_name='id')
    questionnaire_id = sgqlc.types.Field('QuestionnaireIdentity', graphql_name='questionnaireId')
    archived = sgqlc.types.Field('BooleanOperationFilterInput', graphql_name='archived')
    responsible_id = sgqlc.types.Field('ComparableGuidOperationFilterInput', graphql_name='responsibleId')
    web_mode = sgqlc.types.Field('BooleanOperationFilterInput', graphql_name='webMode')
    received_by_tablet_at_utc = sgqlc.types.Field('ComparableNullableOfDateTimeOperationFilterInput', graphql_name='receivedByTabletAtUtc')


class BooleanOperationFilterInput(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('eq', 'neq')
    eq = sgqlc.types.Field(Boolean, graphql_name='eq')
    neq = sgqlc.types.Field(Boolean, graphql_name='neq')


class ComparableDateTimeOperationFilterInput(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('eq', 'neq', 'in_', 'nin', 'gt', 'ngt', 'gte', 'ngte', 'lt', 'nlt', 'lte', 'nlte')
    eq = sgqlc.types.Field(DateTime, graphql_name='eq')
    neq = sgqlc.types.Field(DateTime, graphql_name='neq')
    in_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(DateTime)), graphql_name='in')
    nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(DateTime)), graphql_name='nin')
    gt = sgqlc.types.Field(DateTime, graphql_name='gt')
    ngt = sgqlc.types.Field(DateTime, graphql_name='ngt')
    gte = sgqlc.types.Field(DateTime, graphql_name='gte')
    ngte = sgqlc.types.Field(DateTime, graphql_name='ngte')
    lt = sgqlc.types.Field(DateTime, graphql_name='lt')
    nlt = sgqlc.types.Field(DateTime, graphql_name='nlt')
    lte = sgqlc.types.Field(DateTime, graphql_name='lte')
    nlte = sgqlc.types.Field(DateTime, graphql_name='nlte')


class ComparableGuidOperationFilterInput(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('eq', 'neq', 'in_', 'nin', 'gt', 'ngt', 'gte', 'ngte', 'lt', 'nlt', 'lte', 'nlte')
    eq = sgqlc.types.Field(Uuid, graphql_name='eq')
    neq = sgqlc.types.Field(Uuid, graphql_name='neq')
    in_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Uuid)), graphql_name='in')
    nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Uuid)), graphql_name='nin')
    gt = sgqlc.types.Field(Uuid, graphql_name='gt')
    ngt = sgqlc.types.Field(Uuid, graphql_name='ngt')
    gte = sgqlc.types.Field(Uuid, graphql_name='gte')
    ngte = sgqlc.types.Field(Uuid, graphql_name='ngte')
    lt = sgqlc.types.Field(Uuid, graphql_name='lt')
    nlt = sgqlc.types.Field(Uuid, graphql_name='nlt')
    lte = sgqlc.types.Field(Uuid, graphql_name='lte')
    nlte = sgqlc.types.Field(Uuid, graphql_name='nlte')


class ComparableInt32OperationFilterInput(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('eq', 'neq', 'in_', 'nin', 'gt', 'ngt', 'gte', 'ngte', 'lt', 'nlt', 'lte', 'nlte')
    eq = sgqlc.types.Field(Int, graphql_name='eq')
    neq = sgqlc.types.Field(Int, graphql_name='neq')
    in_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Int)), graphql_name='in')
    nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Int)), graphql_name='nin')
    gt = sgqlc.types.Field(Int, graphql_name='gt')
    ngt = sgqlc.types.Field(Int, graphql_name='ngt')
    gte = sgqlc.types.Field(Int, graphql_name='gte')
    ngte = sgqlc.types.Field(Int, graphql_name='ngte')
    lt = sgqlc.types.Field(Int, graphql_name='lt')
    nlt = sgqlc.types.Field(Int, graphql_name='nlt')
    lte = sgqlc.types.Field(Int, graphql_name='lte')
    nlte = sgqlc.types.Field(Int, graphql_name='nlte')


class ComparableInt64OperationFilterInput(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('eq', 'neq', 'in_', 'nin', 'gt', 'ngt', 'gte', 'ngte', 'lt', 'nlt', 'lte', 'nlte')
    eq = sgqlc.types.Field(Long, graphql_name='eq')
    neq = sgqlc.types.Field(Long, graphql_name='neq')
    in_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Long)), graphql_name='in')
    nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(Long)), graphql_name='nin')
    gt = sgqlc.types.Field(Long, graphql_name='gt')
    ngt = sgqlc.types.Field(Long, graphql_name='ngt')
    gte = sgqlc.types.Field(Long, graphql_name='gte')
    ngte = sgqlc.types.Field(Long, graphql_name='ngte')
    lt = sgqlc.types.Field(Long, graphql_name='lt')
    nlt = sgqlc.types.Field(Long, graphql_name='nlt')
    lte = sgqlc.types.Field(Long, graphql_name='lte')
    nlte = sgqlc.types.Field(Long, graphql_name='nlte')


class ComparableNullableOfDateTimeOperationFilterInput(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('eq', 'neq', 'in_', 'nin', 'gt', 'ngt', 'gte', 'ngte', 'lt', 'nlt', 'lte', 'nlte')
    eq = sgqlc.types.Field(DateTime, graphql_name='eq')
    neq = sgqlc.types.Field(DateTime, graphql_name='neq')
    in_ = sgqlc.types.Field(sgqlc.types.list_of(DateTime), graphql_name='in')
    nin = sgqlc.types.Field(sgqlc.types.list_of(DateTime), graphql_name='nin')
    gt = sgqlc.types.Field(DateTime, graphql_name='gt')
    ngt = sgqlc.types.Field(DateTime, graphql_name='ngt')
    gte = sgqlc.types.Field(DateTime, graphql_name='gte')
    ngte = sgqlc.types.Field(DateTime, graphql_name='ngte')
    lt = sgqlc.types.Field(DateTime, graphql_name='lt')
    nlt = sgqlc.types.Field(DateTime, graphql_name='nlt')
    lte = sgqlc.types.Field(DateTime, graphql_name='lte')
    nlte = sgqlc.types.Field(DateTime, graphql_name='nlte')


class ComparableNullableOfDecimalOperationFilterInput(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('eq', 'neq', 'in_', 'nin', 'gt', 'ngt', 'gte', 'ngte', 'lt', 'nlt', 'lte', 'nlte')
    eq = sgqlc.types.Field(Decimal, graphql_name='eq')
    neq = sgqlc.types.Field(Decimal, graphql_name='neq')
    in_ = sgqlc.types.Field(sgqlc.types.list_of(Decimal), graphql_name='in')
    nin = sgqlc.types.Field(sgqlc.types.list_of(Decimal), graphql_name='nin')
    gt = sgqlc.types.Field(Decimal, graphql_name='gt')
    ngt = sgqlc.types.Field(Decimal, graphql_name='ngt')
    gte = sgqlc.types.Field(Decimal, graphql_name='gte')
    ngte = sgqlc.types.Field(Decimal, graphql_name='ngte')
    lt = sgqlc.types.Field(Decimal, graphql_name='lt')
    nlt = sgqlc.types.Field(Decimal, graphql_name='nlt')
    lte = sgqlc.types.Field(Decimal, graphql_name='lte')
    nlte = sgqlc.types.Field(Decimal, graphql_name='nlte')


class ComparableNullableOfInt32OperationFilterInput(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('eq', 'neq', 'in_', 'nin', 'gt', 'ngt', 'gte', 'ngte', 'lt', 'nlt', 'lte', 'nlte')
    eq = sgqlc.types.Field(Int, graphql_name='eq')
    neq = sgqlc.types.Field(Int, graphql_name='neq')
    in_ = sgqlc.types.Field(sgqlc.types.list_of(Int), graphql_name='in')
    nin = sgqlc.types.Field(sgqlc.types.list_of(Int), graphql_name='nin')
    gt = sgqlc.types.Field(Int, graphql_name='gt')
    ngt = sgqlc.types.Field(Int, graphql_name='ngt')
    gte = sgqlc.types.Field(Int, graphql_name='gte')
    ngte = sgqlc.types.Field(Int, graphql_name='ngte')
    lt = sgqlc.types.Field(Int, graphql_name='lt')
    nlt = sgqlc.types.Field(Int, graphql_name='nlt')
    lte = sgqlc.types.Field(Int, graphql_name='lte')
    nlte = sgqlc.types.Field(Int, graphql_name='nlte')


class IdentifyEntityValueFilter(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('and_', 'or_', 'answer_code', 'value', 'value_lower_case', 'entity')
    and_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('IdentifyEntityValueFilter')), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('IdentifyEntityValueFilter')), graphql_name='or')
    answer_code = sgqlc.types.Field(ComparableNullableOfDecimalOperationFilterInput, graphql_name='answerCode')
    value = sgqlc.types.Field('StringOperationFilterInput', graphql_name='value')
    value_lower_case = sgqlc.types.Field('StringOperationFilterInput', graphql_name='valueLowerCase')
    entity = sgqlc.types.Field('QuestionnaireItemsFilter', graphql_name='entity')


class InterviewFilter(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('and_', 'or_', 'status', 'questionnaire_id', 'questionnaire_variable', 'questionnaire_version', 'key', 'not_answered_count', 'client_key', 'assignment_id', 'created_date', 'responsible_name', 'responsible_name_lower_case', 'supervisor_name', 'supervisor_name_lower_case', 'responsible_role', 'update_date_utc', 'received_by_interviewer_at_utc', 'errors_count', 'identifying_data')
    and_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('InterviewFilter')), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('InterviewFilter')), graphql_name='or')
    status = sgqlc.types.Field('InterviewStatusOperationFilterInput', graphql_name='status')
    questionnaire_id = sgqlc.types.Field(ComparableGuidOperationFilterInput, graphql_name='questionnaireId')
    questionnaire_variable = sgqlc.types.Field('StringOperationFilterInput', graphql_name='questionnaireVariable')
    questionnaire_version = sgqlc.types.Field(ComparableInt64OperationFilterInput, graphql_name='questionnaireVersion')
    key = sgqlc.types.Field('StringOperationFilterInput', graphql_name='key')
    not_answered_count = sgqlc.types.Field(ComparableNullableOfInt32OperationFilterInput, graphql_name='notAnsweredCount')
    client_key = sgqlc.types.Field('StringOperationFilterInput', graphql_name='clientKey')
    assignment_id = sgqlc.types.Field(ComparableNullableOfInt32OperationFilterInput, graphql_name='assignmentId')
    created_date = sgqlc.types.Field(ComparableDateTimeOperationFilterInput, graphql_name='createdDate')
    responsible_name = sgqlc.types.Field('StringOperationFilterInput', graphql_name='responsibleName')
    responsible_name_lower_case = sgqlc.types.Field('StringOperationFilterInput', graphql_name='responsibleNameLowerCase')
    supervisor_name = sgqlc.types.Field('StringOperationFilterInput', graphql_name='supervisorName')
    supervisor_name_lower_case = sgqlc.types.Field('StringOperationFilterInput', graphql_name='supervisorNameLowerCase')
    responsible_role = sgqlc.types.Field('UserRolesOperationFilterInput', graphql_name='responsibleRole')
    update_date_utc = sgqlc.types.Field(ComparableDateTimeOperationFilterInput, graphql_name='updateDateUtc')
    received_by_interviewer_at_utc = sgqlc.types.Field(ComparableNullableOfDateTimeOperationFilterInput, graphql_name='receivedByInterviewerAtUtc')
    errors_count = sgqlc.types.Field(ComparableInt32OperationFilterInput, graphql_name='errorsCount')
    identifying_data = sgqlc.types.Field('ListFilterInputTypeOfIdentifyEntityValueFilterInput', graphql_name='identifyingData')


class InterviewSort(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('key', 'created_date', 'update_date_utc', 'responsible_name', 'responsible_role', 'assignment_id', 'errors_count', 'status', 'received_by_interviewer_at_utc', 'questionnaire_id', 'questionnaire_version', 'id', 'not_answered_count')
    key = sgqlc.types.Field(SortEnumType, graphql_name='key')
    created_date = sgqlc.types.Field(SortEnumType, graphql_name='createdDate')
    update_date_utc = sgqlc.types.Field(SortEnumType, graphql_name='updateDateUtc')
    responsible_name = sgqlc.types.Field(SortEnumType, graphql_name='responsibleName')
    responsible_role = sgqlc.types.Field(SortEnumType, graphql_name='responsibleRole')
    assignment_id = sgqlc.types.Field(SortEnumType, graphql_name='assignmentId')
    errors_count = sgqlc.types.Field(SortEnumType, graphql_name='errorsCount')
    status = sgqlc.types.Field(SortEnumType, graphql_name='status')
    received_by_interviewer_at_utc = sgqlc.types.Field(SortEnumType, graphql_name='receivedByInterviewerAtUtc')
    questionnaire_id = sgqlc.types.Field(SortEnumType, graphql_name='questionnaireId')
    questionnaire_version = sgqlc.types.Field(SortEnumType, graphql_name='questionnaireVersion')
    id = sgqlc.types.Field(SortEnumType, graphql_name='id')
    not_answered_count = sgqlc.types.Field(SortEnumType, graphql_name='notAnsweredCount')


class InterviewStatusOperationFilterInput(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('eq', 'neq', 'in_', 'nin')
    eq = sgqlc.types.Field(InterviewStatus, graphql_name='eq')
    neq = sgqlc.types.Field(InterviewStatus, graphql_name='neq')
    in_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(InterviewStatus)), graphql_name='in')
    nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(InterviewStatus)), graphql_name='nin')


class ListFilterInputTypeOfIdentifyEntityValueFilterInput(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('all', 'none', 'some', 'any')
    all = sgqlc.types.Field(IdentifyEntityValueFilter, graphql_name='all')
    none = sgqlc.types.Field(IdentifyEntityValueFilter, graphql_name='none')
    some = sgqlc.types.Field(IdentifyEntityValueFilter, graphql_name='some')
    any = sgqlc.types.Field(Boolean, graphql_name='any')


class ListFilterInputTypeOfUserMapFilterInput(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('all', 'none', 'some', 'any')
    all = sgqlc.types.Field('UserMapFilterInput', graphql_name='all')
    none = sgqlc.types.Field('UserMapFilterInput', graphql_name='none')
    some = sgqlc.types.Field('UserMapFilterInput', graphql_name='some')
    any = sgqlc.types.Field(Boolean, graphql_name='any')


class MapsFilter(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('and_', 'or_', 'file_name', 'import_date_utc', 'size', 'users')
    and_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('MapsFilter')), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('MapsFilter')), graphql_name='or')
    file_name = sgqlc.types.Field('StringOperationFilterInput', graphql_name='fileName')
    import_date_utc = sgqlc.types.Field(ComparableNullableOfDateTimeOperationFilterInput, graphql_name='importDateUtc')
    size = sgqlc.types.Field(ComparableInt64OperationFilterInput, graphql_name='size')
    users = sgqlc.types.Field(ListFilterInputTypeOfUserMapFilterInput, graphql_name='users')


class MapsSort(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('file_name', 'import_date_utc', 'size')
    file_name = sgqlc.types.Field(SortEnumType, graphql_name='fileName')
    import_date_utc = sgqlc.types.Field(SortEnumType, graphql_name='importDateUtc')
    size = sgqlc.types.Field(SortEnumType, graphql_name='size')


class NullableOfQuestionScopeOperationFilterInput(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('eq', 'neq', 'in_', 'nin')
    eq = sgqlc.types.Field(QuestionScope, graphql_name='eq')
    neq = sgqlc.types.Field(QuestionScope, graphql_name='neq')
    in_ = sgqlc.types.Field(sgqlc.types.list_of(QuestionScope), graphql_name='in')
    nin = sgqlc.types.Field(sgqlc.types.list_of(QuestionScope), graphql_name='nin')


class QuestionFilter(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('and_', 'or_', 'variable', 'scope', 'identifying')
    and_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('QuestionFilter')), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('QuestionFilter')), graphql_name='or')
    variable = sgqlc.types.Field('StringOperationFilterInput', graphql_name='variable')
    scope = sgqlc.types.Field(NullableOfQuestionScopeOperationFilterInput, graphql_name='scope')
    identifying = sgqlc.types.Field(BooleanOperationFilterInput, graphql_name='identifying')


class QuestionnaireIdentity(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('and_', 'or_', 'id', 'version')
    and_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('QuestionnaireIdentity')), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('QuestionnaireIdentity')), graphql_name='or')
    id = sgqlc.types.Field(ComparableGuidOperationFilterInput, graphql_name='id')
    version = sgqlc.types.Field(ComparableInt64OperationFilterInput, graphql_name='version')


class QuestionnaireItemsFilter(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('and_', 'or_', 'title', 'variable', 'scope', 'identifying')
    and_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('QuestionnaireItemsFilter')), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('QuestionnaireItemsFilter')), graphql_name='or')
    title = sgqlc.types.Field('StringOperationFilterInput', graphql_name='title')
    variable = sgqlc.types.Field('StringOperationFilterInput', graphql_name='variable')
    scope = sgqlc.types.Field(NullableOfQuestionScopeOperationFilterInput, graphql_name='scope')
    identifying = sgqlc.types.Field(BooleanOperationFilterInput, graphql_name='identifying')


class StringOperationFilterInput(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('and_', 'or_', 'eq', 'neq', 'contains', 'ncontains', 'in_', 'nin', 'starts_with', 'nstarts_with', 'ends_with', 'nends_with')
    and_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('StringOperationFilterInput')), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('StringOperationFilterInput')), graphql_name='or')
    eq = sgqlc.types.Field(String, graphql_name='eq')
    neq = sgqlc.types.Field(String, graphql_name='neq')
    contains = sgqlc.types.Field(String, graphql_name='contains')
    ncontains = sgqlc.types.Field(String, graphql_name='ncontains')
    in_ = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='in')
    nin = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='nin')
    starts_with = sgqlc.types.Field(String, graphql_name='startsWith')
    nstarts_with = sgqlc.types.Field(String, graphql_name='nstartsWith')
    ends_with = sgqlc.types.Field(String, graphql_name='endsWith')
    nends_with = sgqlc.types.Field(String, graphql_name='nendsWith')


class StringOperationFilterInputType(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('and_', 'or_', 'eq', 'neq', 'contains', 'ncontains', 'in_', 'nin', 'starts_with', 'nstarts_with')
    and_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('StringOperationFilterInputType')), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('StringOperationFilterInputType')), graphql_name='or')
    eq = sgqlc.types.Field(String, graphql_name='eq')
    neq = sgqlc.types.Field(String, graphql_name='neq')
    contains = sgqlc.types.Field(String, graphql_name='contains')
    ncontains = sgqlc.types.Field(String, graphql_name='ncontains')
    in_ = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='in')
    nin = sgqlc.types.Field(sgqlc.types.list_of(String), graphql_name='nin')
    starts_with = sgqlc.types.Field(String, graphql_name='startsWith')
    nstarts_with = sgqlc.types.Field(String, graphql_name='nstartsWith')


class UserMapFilterInput(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('and_', 'or_', 'id', 'user_name', 'map')
    and_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('UserMapFilterInput')), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('UserMapFilterInput')), graphql_name='or')
    id = sgqlc.types.Field(ComparableInt32OperationFilterInput, graphql_name='id')
    user_name = sgqlc.types.Field(StringOperationFilterInput, graphql_name='userName')
    map = sgqlc.types.Field(MapsFilter, graphql_name='map')


class UserRolesOperationFilterInput(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('eq', 'neq', 'in_', 'nin')
    eq = sgqlc.types.Field(UserRoles, graphql_name='eq')
    neq = sgqlc.types.Field(UserRoles, graphql_name='neq')
    in_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(UserRoles)), graphql_name='in')
    nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(UserRoles)), graphql_name='nin')



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


class CalendarEvent(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('assignment_id', 'comment', 'creator_user_id', 'interview_id', 'interview_key', 'is_completed', 'public_key', 'start_timezone', 'start_utc', 'update_date_utc')
    assignment_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='assignmentId')
    comment = sgqlc.types.Field(String, graphql_name='comment')
    creator_user_id = sgqlc.types.Field(sgqlc.types.non_null(Uuid), graphql_name='creatorUserId')
    interview_id = sgqlc.types.Field(Uuid, graphql_name='interviewId')
    interview_key = sgqlc.types.Field(String, graphql_name='interviewKey')
    is_completed = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isCompleted')
    public_key = sgqlc.types.Field(sgqlc.types.non_null(Uuid), graphql_name='publicKey')
    start_timezone = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='startTimezone')
    start_utc = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='startUtc')
    update_date_utc = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='updateDateUtc')


class CategoricalOption(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('parent_value', 'title', 'value')
    parent_value = sgqlc.types.Field(Int, graphql_name='parentValue')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    value = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='value')


class Entity(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('identifying', 'label', 'options', 'question_text', 'scope', 'type', 'variable')
    identifying = sgqlc.types.Field(Boolean, graphql_name='identifying')
    label = sgqlc.types.Field(String, graphql_name='label')
    options = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(CategoricalOption))), graphql_name='options')
    question_text = sgqlc.types.Field(String, graphql_name='questionText')
    scope = sgqlc.types.Field(QuestionScope, graphql_name='scope')
    type = sgqlc.types.Field(sgqlc.types.non_null(QuestionType), graphql_name='type')
    variable = sgqlc.types.Field(String, graphql_name='variable')


class HeadquartersMutation(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('add_or_update_calendar_event', 'delete_calendar_event', 'delete_map', 'delete_user_from_map', 'add_user_to_map')
    add_or_update_calendar_event = sgqlc.types.Field(CalendarEvent, graphql_name='addOrUpdateCalendarEvent', args=sgqlc.types.ArgDict((
        ('workspace', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='workspace', default='primary')),
        ('assignment_id', sgqlc.types.Arg(Int, graphql_name='assignmentId', default=None)),
        ('comment', sgqlc.types.Arg(String, graphql_name='comment', default=None)),
        ('interview_id', sgqlc.types.Arg(Uuid, graphql_name='interviewId', default=None)),
        ('interview_key', sgqlc.types.Arg(String, graphql_name='interviewKey', default=None)),
        ('new_start', sgqlc.types.Arg(DateTime, graphql_name='newStart', default=None)),
        ('public_key', sgqlc.types.Arg(Uuid, graphql_name='publicKey', default=None)),
        ('start_timezone', sgqlc.types.Arg(String, graphql_name='startTimezone', default=None)),
))
    )
    delete_calendar_event = sgqlc.types.Field(CalendarEvent, graphql_name='deleteCalendarEvent', args=sgqlc.types.ArgDict((
        ('workspace', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='workspace', default='primary')),
        ('public_key', sgqlc.types.Arg(sgqlc.types.non_null(Uuid), graphql_name='publicKey', default=None)),
))
    )
    delete_map = sgqlc.types.Field('Map', graphql_name='deleteMap', args=sgqlc.types.ArgDict((
        ('workspace', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='workspace', default='primary')),
        ('file_name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='fileName', default=None)),
))
    )
    delete_user_from_map = sgqlc.types.Field('Map', graphql_name='deleteUserFromMap', args=sgqlc.types.ArgDict((
        ('workspace', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='workspace', default='primary')),
        ('file_name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='fileName', default=None)),
        ('user_name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='userName', default=None)),
))
    )
    add_user_to_map = sgqlc.types.Field('Map', graphql_name='addUserToMap', args=sgqlc.types.ArgDict((
        ('workspace', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='workspace', default='primary')),
        ('file_name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='fileName', default=None)),
        ('user_name', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='userName', default=None)),
))
    )


class HeadquartersQuery(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('assignments', 'interviews', 'maps', 'questionnaires', 'questions', 'questionnaire_items', 'viewer')
    assignments = sgqlc.types.Field('IPagedConnectionOfAssignment', graphql_name='assignments', args=sgqlc.types.ArgDict((
        ('workspace', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='workspace', default='primary')),
        ('skip', sgqlc.types.Arg(Int, graphql_name='skip', default=None)),
        ('take', sgqlc.types.Arg(Int, graphql_name='take', default=None)),
        ('where', sgqlc.types.Arg(AssignmentsFilter, graphql_name='where', default=None)),
))
    )
    interviews = sgqlc.types.Field('IPagedConnectionOfInterview', graphql_name='interviews', args=sgqlc.types.ArgDict((
        ('workspace', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='workspace', default='primary')),
        ('skip', sgqlc.types.Arg(Int, graphql_name='skip', default=None)),
        ('take', sgqlc.types.Arg(Int, graphql_name='take', default=None)),
        ('where', sgqlc.types.Arg(InterviewFilter, graphql_name='where', default=None)),
        ('order', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(InterviewSort)), graphql_name='order', default=None)),
))
    )
    maps = sgqlc.types.Field('IPagedConnectionOfMap', graphql_name='maps', args=sgqlc.types.ArgDict((
        ('workspace', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='workspace', default='primary')),
        ('skip', sgqlc.types.Arg(Int, graphql_name='skip', default=None)),
        ('take', sgqlc.types.Arg(Int, graphql_name='take', default=None)),
        ('where', sgqlc.types.Arg(MapsFilter, graphql_name='where', default=None)),
        ('order', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(MapsSort)), graphql_name='order', default=None)),
))
    )
    questionnaires = sgqlc.types.Field('IPagedConnectionOfQuestionnaire', graphql_name='questionnaires', args=sgqlc.types.ArgDict((
        ('workspace', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='workspace', default='primary')),
        ('skip', sgqlc.types.Arg(Int, graphql_name='skip', default=None)),
        ('take', sgqlc.types.Arg(Int, graphql_name='take', default=None)),
        ('id', sgqlc.types.Arg(Uuid, graphql_name='id', default=None)),
        ('version', sgqlc.types.Arg(Long, graphql_name='version', default=None)),
))
    )
    questions = sgqlc.types.Field(sgqlc.types.list_of(Entity), graphql_name='questions', args=sgqlc.types.ArgDict((
        ('workspace', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='workspace', default='primary')),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(Uuid), graphql_name='id', default=None)),
        ('version', sgqlc.types.Arg(sgqlc.types.non_null(Long), graphql_name='version', default=None)),
        ('language', sgqlc.types.Arg(String, graphql_name='language', default=None)),
        ('where', sgqlc.types.Arg(QuestionFilter, graphql_name='where', default=None)),
))
    )
    questionnaire_items = sgqlc.types.Field(sgqlc.types.list_of('QuestionnaireItem'), graphql_name='questionnaireItems', args=sgqlc.types.ArgDict((
        ('workspace', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='workspace', default='primary')),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(Uuid), graphql_name='id', default=None)),
        ('version', sgqlc.types.Arg(sgqlc.types.non_null(Long), graphql_name='version', default=None)),
        ('language', sgqlc.types.Arg(String, graphql_name='language', default=None)),
        ('where', sgqlc.types.Arg(QuestionnaireItemsFilter, graphql_name='where', default=None)),
))
    )
    viewer = sgqlc.types.Field('User', graphql_name='viewer')


class IPagedConnectionOfAssignment(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('nodes', 'total_count', 'filtered_count')
    nodes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(Assignment)), graphql_name='nodes')
    total_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalCount')
    filtered_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='filteredCount')


class IPagedConnectionOfInterview(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('nodes', 'total_count', 'filtered_count')
    nodes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('Interview')), graphql_name='nodes')
    total_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalCount')
    filtered_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='filteredCount')


class IPagedConnectionOfMap(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('nodes', 'total_count', 'filtered_count')
    nodes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('Map')), graphql_name='nodes')
    total_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalCount')
    filtered_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='filteredCount')


class IPagedConnectionOfQuestionnaire(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('nodes', 'total_count', 'filtered_count')
    nodes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of('Questionnaire')), graphql_name='nodes')
    total_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalCount')
    filtered_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='filteredCount')


class IdentifyingEntity(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('answer_value', 'entity', 'value')
    answer_value = sgqlc.types.Field(Int, graphql_name='answerValue')
    entity = sgqlc.types.Field(sgqlc.types.non_null(Entity), graphql_name='entity')
    value = sgqlc.types.Field(String, graphql_name='value')


class Interview(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('action_flags', 'assignment_id', 'id', 'status', 'responsible_name', 'responsible_id', 'responsible_role', 'supervisor_name', 'was_completed', 'created_date', 'key', 'client_key', 'update_date_utc', 'received_by_interviewer_at_utc', 'errors_count', 'questionnaire_id', 'questionnaire_variable', 'questionnaire_version', 'identifying_data', 'not_answered_count', 'calendar_event')
    action_flags = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(InterviewActionFlags))), graphql_name='actionFlags')
    assignment_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='assignmentId')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    status = sgqlc.types.Field(sgqlc.types.non_null(InterviewStatus), graphql_name='status')
    responsible_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='responsibleName')
    responsible_id = sgqlc.types.Field(sgqlc.types.non_null(Uuid), graphql_name='responsibleId')
    responsible_role = sgqlc.types.Field(sgqlc.types.non_null(UserRoles), graphql_name='responsibleRole')
    supervisor_name = sgqlc.types.Field(String, graphql_name='supervisorName')
    was_completed = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='wasCompleted')
    created_date = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='createdDate')
    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='key')
    client_key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='clientKey')
    update_date_utc = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='updateDateUtc')
    received_by_interviewer_at_utc = sgqlc.types.Field(DateTime, graphql_name='receivedByInterviewerAtUtc')
    errors_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='errorsCount')
    questionnaire_id = sgqlc.types.Field(sgqlc.types.non_null(Uuid), graphql_name='questionnaireId')
    questionnaire_variable = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='questionnaireVariable')
    questionnaire_version = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='questionnaireVersion')
    identifying_data = sgqlc.types.Field(sgqlc.types.list_of(IdentifyingEntity), graphql_name='identifyingData')
    not_answered_count = sgqlc.types.Field(Int, graphql_name='notAnsweredCount')
    calendar_event = sgqlc.types.Field(CalendarEvent, graphql_name='calendarEvent')


class Map(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('file_name', 'size', 'import_date', 'users', 'x_max_val', 'y_max_val', 'x_min_val', 'y_min_val', 'wkid', 'max_scale', 'min_scale')
    file_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='fileName')
    size = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='size')
    import_date = sgqlc.types.Field(DateTime, graphql_name='importDate')
    users = sgqlc.types.Field(sgqlc.types.list_of('UserMap'), graphql_name='users')
    x_max_val = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='xMaxVal')
    y_max_val = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='yMaxVal')
    x_min_val = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='xMinVal')
    y_min_val = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='yMinVal')
    wkid = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='wkid')
    max_scale = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='maxScale')
    min_scale = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='minScale')


class Questionnaire(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('variable', 'questionnaire_id', 'version', 'id', 'title', 'default_language_name', 'translations')
    variable = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='variable')
    questionnaire_id = sgqlc.types.Field(sgqlc.types.non_null(Uuid), graphql_name='questionnaireId')
    version = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='version')
    id = sgqlc.types.Field(ID, graphql_name='id')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    default_language_name = sgqlc.types.Field(String, graphql_name='defaultLanguageName')
    translations = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Translation'))), graphql_name='translations')


class QuestionnaireItem(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('entity_type', 'title', 'variable', 'scope', 'label', 'type', 'identifying', 'options')
    entity_type = sgqlc.types.Field(EntityType, graphql_name='entityType')
    title = sgqlc.types.Field(String, graphql_name='title')
    variable = sgqlc.types.Field(String, graphql_name='variable')
    scope = sgqlc.types.Field(QuestionScope, graphql_name='scope')
    label = sgqlc.types.Field(String, graphql_name='label')
    type = sgqlc.types.Field(QuestionType, graphql_name='type')
    identifying = sgqlc.types.Field(Boolean, graphql_name='identifying')
    options = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(CategoricalOption))), graphql_name='options')


class Translation(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('id', 'name')
    id = sgqlc.types.Field(sgqlc.types.non_null(Uuid), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')


class User(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('id', 'roles', 'user_name', 'workspaces')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    roles = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(UserRoles))), graphql_name='roles')
    user_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='userName')
    workspaces = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='workspaces')


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
headquarters_schema.mutation_type = HeadquartersMutation
headquarters_schema.subscription_type = None

