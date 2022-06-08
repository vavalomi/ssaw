import sgqlc.types
import sgqlc.types.datetime


headquarters_schema = sgqlc.types.Schema()



########################################################################
# Scalars and Enumerations
########################################################################
class Any(sgqlc.types.Scalar):
    __schema__ = headquarters_schema


class ApplyPolicy(sgqlc.types.Enum):
    __schema__ = headquarters_schema
    __choices__ = ('AFTER_RESOLVER', 'BEFORE_RESOLVER')


Boolean = sgqlc.types.Boolean

Date = sgqlc.types.datetime.Date

DateTime = sgqlc.types.datetime.DateTime

class Decimal(sgqlc.types.Scalar):
    __schema__ = headquarters_schema


class EntityType(sgqlc.types.Enum):
    __schema__ = headquarters_schema
    __choices__ = ('QUESTION', 'ROSTER', 'SECTION', 'STATICTEXT', 'VARIABLE')


Float = sgqlc.types.Float

class GeoJSONObjectType(sgqlc.types.Enum):
    __schema__ = headquarters_schema
    __choices__ = ('Feature', 'FeatureCollection', 'GeometryCollection', 'LineString', 'MultiLineString', 'MultiPoint', 'MultiPolygon', 'Point', 'Polygon')


ID = sgqlc.types.ID

Int = sgqlc.types.Int

class InterviewActionFlags(sgqlc.types.Enum):
    __schema__ = headquarters_schema
    __choices__ = ('CANBEAPPROVED', 'CANBEDELETED', 'CANBEOPENED', 'CANBEREASSIGNED', 'CANBEREJECTED', 'CANBERESTARTED', 'CANBEUNAPPROVEDBYHQ', 'CANCHANGETOCAPI', 'CANCHANGETOCAWI')


class InterviewMode(sgqlc.types.Enum):
    __schema__ = headquarters_schema
    __choices__ = ('CAPI', 'CAWI', 'UNKNOWN')


class InterviewStatus(sgqlc.types.Enum):
    __schema__ = headquarters_schema
    __choices__ = ('APPROVEDBYHEADQUARTERS', 'APPROVEDBYSUPERVISOR', 'COMPLETED', 'CREATED', 'DELETED', 'INTERVIEWERASSIGNED', 'READYFORINTERVIEW', 'REJECTEDBYHEADQUARTERS', 'REJECTEDBYSUPERVISOR', 'RESTARTED', 'RESTORED', 'SENTTOCAPI', 'SUPERVISORASSIGNED')


class Long(sgqlc.types.Scalar):
    __schema__ = headquarters_schema


class QuestionScope(sgqlc.types.Enum):
    __schema__ = headquarters_schema
    __choices__ = ('HEADQUARTER', 'HIDDEN', 'INTERVIEWER', 'SUPERVISOR')


class QuestionType(sgqlc.types.Enum):
    __schema__ = headquarters_schema
    __choices__ = ('AREA', 'AUDIO', 'DATETIME', 'GPSCOORDINATES', 'MULTIMEDIA', 'MULTYOPTION', 'NUMERIC', 'QRBARCODE', 'SINGLEOPTION', 'TEXT', 'TEXTLIST')


class SortEnumType(sgqlc.types.Enum):
    __schema__ = headquarters_schema
    __choices__ = ('ASC', 'DESC')


String = sgqlc.types.String

class UUID(sgqlc.types.Scalar):
    __schema__ = headquarters_schema


class Upload(sgqlc.types.Scalar):
    __schema__ = headquarters_schema


class UserRoles(sgqlc.types.Enum):
    __schema__ = headquarters_schema
    __choices__ = ('ADMINISTRATOR', 'APIUSER', 'HEADQUARTER', 'INTERVIEWER', 'OBSERVER', 'SUPERVISOR')


class VariableType(sgqlc.types.Enum):
    __schema__ = headquarters_schema
    __choices__ = ('BOOLEAN', 'DATETIME', 'DOUBLE', 'LONGINTEGER', 'STRING')



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
    eq = sgqlc.types.Field(UUID, graphql_name='eq')
    neq = sgqlc.types.Field(UUID, graphql_name='neq')
    in_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(UUID)), graphql_name='in')
    nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(UUID)), graphql_name='nin')
    gt = sgqlc.types.Field(UUID, graphql_name='gt')
    ngt = sgqlc.types.Field(UUID, graphql_name='ngt')
    gte = sgqlc.types.Field(UUID, graphql_name='gte')
    ngte = sgqlc.types.Field(UUID, graphql_name='ngte')
    lt = sgqlc.types.Field(UUID, graphql_name='lt')
    nlt = sgqlc.types.Field(UUID, graphql_name='nlt')
    lte = sgqlc.types.Field(UUID, graphql_name='lte')
    nlte = sgqlc.types.Field(UUID, graphql_name='nlte')


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


class ComparableNullableOfDoubleOperationFilterInput(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('eq', 'neq', 'in_', 'nin', 'gt', 'ngt', 'gte', 'ngte', 'lt', 'nlt', 'lte', 'nlte')
    eq = sgqlc.types.Field(Float, graphql_name='eq')
    neq = sgqlc.types.Field(Float, graphql_name='neq')
    in_ = sgqlc.types.Field(sgqlc.types.list_of(Float), graphql_name='in')
    nin = sgqlc.types.Field(sgqlc.types.list_of(Float), graphql_name='nin')
    gt = sgqlc.types.Field(Float, graphql_name='gt')
    ngt = sgqlc.types.Field(Float, graphql_name='ngt')
    gte = sgqlc.types.Field(Float, graphql_name='gte')
    ngte = sgqlc.types.Field(Float, graphql_name='ngte')
    lt = sgqlc.types.Field(Float, graphql_name='lt')
    nlt = sgqlc.types.Field(Float, graphql_name='nlt')
    lte = sgqlc.types.Field(Float, graphql_name='lte')
    nlte = sgqlc.types.Field(Float, graphql_name='nlte')


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


class ComparableNullableOfInt64OperationFilterInput(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('eq', 'neq', 'in_', 'nin', 'gt', 'ngt', 'gte', 'ngte', 'lt', 'nlt', 'lte', 'nlte')
    eq = sgqlc.types.Field(Long, graphql_name='eq')
    neq = sgqlc.types.Field(Long, graphql_name='neq')
    in_ = sgqlc.types.Field(sgqlc.types.list_of(Long), graphql_name='in')
    nin = sgqlc.types.Field(sgqlc.types.list_of(Long), graphql_name='nin')
    gt = sgqlc.types.Field(Long, graphql_name='gt')
    ngt = sgqlc.types.Field(Long, graphql_name='ngt')
    gte = sgqlc.types.Field(Long, graphql_name='gte')
    ngte = sgqlc.types.Field(Long, graphql_name='ngte')
    lt = sgqlc.types.Field(Long, graphql_name='lt')
    nlt = sgqlc.types.Field(Long, graphql_name='nlt')
    lte = sgqlc.types.Field(Long, graphql_name='lte')
    nlte = sgqlc.types.Field(Long, graphql_name='nlte')


class IdentifyEntityValueFilter(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('and_', 'or_', 'answer_code', 'value', 'value_lower_case', 'entity', 'value_bool', 'value_date', 'value_double', 'value_long', 'is_enabled')
    and_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('IdentifyEntityValueFilter')), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('IdentifyEntityValueFilter')), graphql_name='or')
    answer_code = sgqlc.types.Field(ComparableNullableOfDecimalOperationFilterInput, graphql_name='answerCode')
    value = sgqlc.types.Field('StringOperationFilterInput', graphql_name='value')
    value_lower_case = sgqlc.types.Field('StringOperationFilterInput', graphql_name='valueLowerCase')
    entity = sgqlc.types.Field('QuestionnaireItemsFilter', graphql_name='entity')
    value_bool = sgqlc.types.Field(BooleanOperationFilterInput, graphql_name='valueBool')
    value_date = sgqlc.types.Field(ComparableNullableOfDateTimeOperationFilterInput, graphql_name='valueDate')
    value_double = sgqlc.types.Field(ComparableNullableOfDoubleOperationFilterInput, graphql_name='valueDouble')
    value_long = sgqlc.types.Field(ComparableNullableOfInt64OperationFilterInput, graphql_name='valueLong')
    is_enabled = sgqlc.types.Field(BooleanOperationFilterInput, graphql_name='isEnabled')


class InterviewModeOperationFilterInput(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('eq', 'neq', 'in_', 'nin')
    eq = sgqlc.types.Field(InterviewMode, graphql_name='eq')
    neq = sgqlc.types.Field(InterviewMode, graphql_name='neq')
    in_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(InterviewMode)), graphql_name='in')
    nin = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null(InterviewMode)), graphql_name='nin')


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


class InterviewsFilter(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('and_', 'or_', 'status', 'interview_mode', 'questionnaire_id', 'questionnaire_variable', 'questionnaire_version', 'key', 'not_answered_count', 'client_key', 'assignment_id', 'created_date', 'responsible_name', 'supervisor_name', 'responsible_role', 'update_date_utc', 'received_by_interviewer_at_utc', 'errors_count', 'identifying_data')
    and_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('InterviewsFilter')), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('InterviewsFilter')), graphql_name='or')
    status = sgqlc.types.Field(InterviewStatusOperationFilterInput, graphql_name='status')
    interview_mode = sgqlc.types.Field(InterviewModeOperationFilterInput, graphql_name='interviewMode')
    questionnaire_id = sgqlc.types.Field(ComparableGuidOperationFilterInput, graphql_name='questionnaireId')
    questionnaire_variable = sgqlc.types.Field('StringOperationFilterInput', graphql_name='questionnaireVariable')
    questionnaire_version = sgqlc.types.Field(ComparableInt64OperationFilterInput, graphql_name='questionnaireVersion')
    key = sgqlc.types.Field('StringOperationFilterInput', graphql_name='key')
    not_answered_count = sgqlc.types.Field(ComparableNullableOfInt32OperationFilterInput, graphql_name='notAnsweredCount')
    client_key = sgqlc.types.Field('StringOperationFilterInput', graphql_name='clientKey')
    assignment_id = sgqlc.types.Field(ComparableNullableOfInt32OperationFilterInput, graphql_name='assignmentId')
    created_date = sgqlc.types.Field(ComparableDateTimeOperationFilterInput, graphql_name='createdDate')
    responsible_name = sgqlc.types.Field('StringOperationFilterInput', graphql_name='responsibleNameLowerCase')
    supervisor_name = sgqlc.types.Field('StringOperationFilterInput', graphql_name='supervisorNameLowerCase')
    responsible_role = sgqlc.types.Field('UserRolesOperationFilterInput', graphql_name='responsibleRole')
    update_date_utc = sgqlc.types.Field(ComparableDateTimeOperationFilterInput, graphql_name='updateDateUtc')
    received_by_interviewer_at_utc = sgqlc.types.Field(ComparableNullableOfDateTimeOperationFilterInput, graphql_name='receivedByInterviewerAtUtc')
    errors_count = sgqlc.types.Field(ComparableInt32OperationFilterInput, graphql_name='errorsCount')
    identifying_data = sgqlc.types.Field('ListFilterInputTypeOfIdentifyEntityValueFilterInput', graphql_name='identifyingData')


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


class MapReportFilter(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('and_', 'or_', 'interview_filter')
    and_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('MapReportFilter')), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('MapReportFilter')), graphql_name='or')
    interview_filter = sgqlc.types.Field(InterviewsFilter, graphql_name='interviewFilter')


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
    __field_names__ = ('and_', 'or_', 'title', 'variable', 'scope', 'identifying', 'included_in_reporting_at_utc')
    and_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('QuestionnaireItemsFilter')), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('QuestionnaireItemsFilter')), graphql_name='or')
    title = sgqlc.types.Field('StringOperationFilterInput', graphql_name='title')
    variable = sgqlc.types.Field('StringOperationFilterInput', graphql_name='variable')
    scope = sgqlc.types.Field(NullableOfQuestionScopeOperationFilterInput, graphql_name='scope')
    identifying = sgqlc.types.Field(BooleanOperationFilterInput, graphql_name='identifying')
    included_in_reporting_at_utc = sgqlc.types.Field(ComparableNullableOfDateTimeOperationFilterInput, graphql_name='includedInReportingAtUtc')


class RoleFilterInput(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('and_', 'or_', 'eq')
    and_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('RoleFilterInput')), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('RoleFilterInput')), graphql_name='or')
    eq = sgqlc.types.Field(UserRoles, graphql_name='eq')


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


class UsersFilterInput(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('and_', 'or_', 'user_name', 'full_name', 'is_archived', 'is_locked', 'creation_date', 'email', 'phone_number', 'id', 'role')
    and_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('UsersFilterInput')), graphql_name='and')
    or_ = sgqlc.types.Field(sgqlc.types.list_of(sgqlc.types.non_null('UsersFilterInput')), graphql_name='or')
    user_name = sgqlc.types.Field(StringOperationFilterInput, graphql_name='userName')
    full_name = sgqlc.types.Field(StringOperationFilterInput, graphql_name='fullName')
    is_archived = sgqlc.types.Field(BooleanOperationFilterInput, graphql_name='isArchived')
    is_locked = sgqlc.types.Field(BooleanOperationFilterInput, graphql_name='isLocked')
    creation_date = sgqlc.types.Field(ComparableDateTimeOperationFilterInput, graphql_name='creationDate')
    email = sgqlc.types.Field(StringOperationFilterInput, graphql_name='email')
    phone_number = sgqlc.types.Field(StringOperationFilterInput, graphql_name='phoneNumber')
    id = sgqlc.types.Field(ComparableGuidOperationFilterInput, graphql_name='id')
    role = sgqlc.types.Field(RoleFilterInput, graphql_name='role')


class UsersSortInput(sgqlc.types.Input):
    __schema__ = headquarters_schema
    __field_names__ = ('user_name', 'creation_date', 'full_name', 'role', 'email', 'phone_number', 'is_locked', 'is_archived')
    user_name = sgqlc.types.Field(SortEnumType, graphql_name='userName')
    creation_date = sgqlc.types.Field(SortEnumType, graphql_name='creationDate')
    full_name = sgqlc.types.Field(SortEnumType, graphql_name='fullName')
    role = sgqlc.types.Field(SortEnumType, graphql_name='role')
    email = sgqlc.types.Field(SortEnumType, graphql_name='email')
    phone_number = sgqlc.types.Field(SortEnumType, graphql_name='phoneNumber')
    is_locked = sgqlc.types.Field(SortEnumType, graphql_name='isLocked')
    is_archived = sgqlc.types.Field(SortEnumType, graphql_name='isArchived')



########################################################################
# Output Objects and Interfaces
########################################################################
class Assignment(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('archived', 'created_at_utc', 'email', 'id', 'interviews_needed', 'received_by_tablet_at_utc', 'responsible_id', 'web_mode', 'calendar_event')
    archived = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='archived')
    created_at_utc = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='createdAtUtc')
    email = sgqlc.types.Field(String, graphql_name='email')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    interviews_needed = sgqlc.types.Field(Int, graphql_name='interviewsNeeded')
    received_by_tablet_at_utc = sgqlc.types.Field(DateTime, graphql_name='receivedByTabletAtUtc')
    responsible_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='responsibleId')
    web_mode = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='webMode')
    calendar_event = sgqlc.types.Field('CalendarEvent', graphql_name='calendarEvent')


class CalendarEvent(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('assignment_id', 'comment', 'creator_user_id', 'interview_id', 'interview_key', 'is_completed', 'public_key', 'start_timezone', 'start_utc', 'update_date_utc')
    assignment_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='assignmentId')
    comment = sgqlc.types.Field(String, graphql_name='comment')
    creator_user_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='creatorUserId')
    interview_id = sgqlc.types.Field(UUID, graphql_name='interviewId')
    interview_key = sgqlc.types.Field(String, graphql_name='interviewKey')
    is_completed = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='isCompleted')
    public_key = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='publicKey')
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
    __field_names__ = ('identifying', 'label', 'options', 'question_text', 'scope', 'type', 'variable', 'variable_type')
    identifying = sgqlc.types.Field(Boolean, graphql_name='identifying')
    label = sgqlc.types.Field(String, graphql_name='label')
    options = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(CategoricalOption))), graphql_name='options')
    question_text = sgqlc.types.Field(String, graphql_name='questionText')
    scope = sgqlc.types.Field(QuestionScope, graphql_name='scope')
    type = sgqlc.types.Field(QuestionType, graphql_name='type')
    variable = sgqlc.types.Field(String, graphql_name='variable')
    variable_type = sgqlc.types.Field(VariableType, graphql_name='variableType')


class Feature(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('type', 'id', 'geometry', 'properties')
    type = sgqlc.types.Field(sgqlc.types.non_null(GeoJSONObjectType), graphql_name='type')
    id = sgqlc.types.Field(String, graphql_name='id')
    geometry = sgqlc.types.Field(Any, graphql_name='geometry')
    properties = sgqlc.types.Field(Any, graphql_name='properties')


class FeatureCollection(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('features', 'type')
    features = sgqlc.types.Field(sgqlc.types.list_of(Feature), graphql_name='features')
    type = sgqlc.types.Field(sgqlc.types.non_null(GeoJSONObjectType), graphql_name='type')


class GeoBounds(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('north', 'south', 'east', 'west')
    north = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='north')
    south = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='south')
    east = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='east')
    west = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='west')


class HeadquartersMutation(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('update_calendar_event', 'delete_calendar_event', 'add_assignment_calendar_event', 'add_interview_calendar_event', 'delete_map', 'delete_user_from_map', 'add_user_to_map', 'upload_map')
    update_calendar_event = sgqlc.types.Field(CalendarEvent, graphql_name='updateCalendarEvent', args=sgqlc.types.ArgDict((
        ('workspace', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='workspace', default='primary')),
        ('comment', sgqlc.types.Arg(String, graphql_name='comment', default=None)),
        ('new_start', sgqlc.types.Arg(sgqlc.types.non_null(DateTime), graphql_name='newStart', default=None)),
        ('public_key', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='publicKey', default=None)),
        ('start_timezone', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='startTimezone', default=None)),
))
    )
    delete_calendar_event = sgqlc.types.Field(CalendarEvent, graphql_name='deleteCalendarEvent', args=sgqlc.types.ArgDict((
        ('workspace', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='workspace', default='primary')),
        ('public_key', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='publicKey', default=None)),
))
    )
    add_assignment_calendar_event = sgqlc.types.Field(CalendarEvent, graphql_name='addAssignmentCalendarEvent', args=sgqlc.types.ArgDict((
        ('workspace', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='workspace', default='primary')),
        ('assignment_id', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='assignmentId', default=None)),
        ('comment', sgqlc.types.Arg(String, graphql_name='comment', default=None)),
        ('new_start', sgqlc.types.Arg(sgqlc.types.non_null(DateTime), graphql_name='newStart', default=None)),
        ('start_timezone', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='startTimezone', default=None)),
))
    )
    add_interview_calendar_event = sgqlc.types.Field(CalendarEvent, graphql_name='addInterviewCalendarEvent', args=sgqlc.types.ArgDict((
        ('workspace', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='workspace', default='primary')),
        ('comment', sgqlc.types.Arg(String, graphql_name='comment', default=None)),
        ('interview_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='interviewId', default=None)),
        ('new_start', sgqlc.types.Arg(sgqlc.types.non_null(DateTime), graphql_name='newStart', default=None)),
        ('start_timezone', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='startTimezone', default=None)),
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
    upload_map = sgqlc.types.Field(sgqlc.types.list_of('Map'), graphql_name='uploadMap', args=sgqlc.types.ArgDict((
        ('workspace', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='workspace', default='primary')),
        ('file', sgqlc.types.Arg(sgqlc.types.non_null(Upload), graphql_name='file', default=None)),
))
    )


class HeadquartersQuery(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('assignments', 'interviews', 'maps', 'questionnaires', 'questions', 'questionnaire_items', 'viewer', 'users', 'map_report')
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
        ('where', sgqlc.types.Arg(InterviewsFilter, graphql_name='where', default=None)),
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
        ('id', sgqlc.types.Arg(UUID, graphql_name='id', default=None)),
        ('version', sgqlc.types.Arg(Long, graphql_name='version', default=None)),
))
    )
    questions = sgqlc.types.Field(sgqlc.types.list_of(Entity), graphql_name='questions', args=sgqlc.types.ArgDict((
        ('workspace', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='workspace', default='primary')),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='id', default=None)),
        ('version', sgqlc.types.Arg(sgqlc.types.non_null(Long), graphql_name='version', default=None)),
        ('language', sgqlc.types.Arg(String, graphql_name='language', default=None)),
        ('where', sgqlc.types.Arg(QuestionFilter, graphql_name='where', default=None)),
))
    )
    questionnaire_items = sgqlc.types.Field(sgqlc.types.list_of('QuestionnaireItem'), graphql_name='questionnaireItems', args=sgqlc.types.ArgDict((
        ('workspace', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='workspace', default='primary')),
        ('id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='id', default=None)),
        ('version', sgqlc.types.Arg(sgqlc.types.non_null(Long), graphql_name='version', default=None)),
        ('language', sgqlc.types.Arg(String, graphql_name='language', default=None)),
        ('where', sgqlc.types.Arg(QuestionnaireItemsFilter, graphql_name='where', default=None)),
))
    )
    viewer = sgqlc.types.Field('Viewer', graphql_name='viewer')
    users = sgqlc.types.Field('Users', graphql_name='users', args=sgqlc.types.ArgDict((
        ('skip', sgqlc.types.Arg(Int, graphql_name='skip', default=None)),
        ('take', sgqlc.types.Arg(Int, graphql_name='take', default=None)),
        ('order', sgqlc.types.Arg(sgqlc.types.list_of(sgqlc.types.non_null(UsersSortInput)), graphql_name='order', default=None)),
        ('where', sgqlc.types.Arg(UsersFilterInput, graphql_name='where', default=None)),
))
    )
    map_report = sgqlc.types.Field('MapReportHolder', graphql_name='mapReport', args=sgqlc.types.ArgDict((
        ('workspace', sgqlc.types.Arg(sgqlc.types.non_null(String), graphql_name='workspace', default='primary')),
        ('questionnaire_id', sgqlc.types.Arg(sgqlc.types.non_null(UUID), graphql_name='questionnaireId', default=None)),
        ('questionnaire_version', sgqlc.types.Arg(Long, graphql_name='questionnaireVersion', default=None)),
        ('variable', sgqlc.types.Arg(String, graphql_name='variable', default=None)),
        ('zoom', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='zoom', default=None)),
        ('client_map_width', sgqlc.types.Arg(sgqlc.types.non_null(Int), graphql_name='clientMapWidth', default=None)),
        ('east', sgqlc.types.Arg(sgqlc.types.non_null(Float), graphql_name='east', default=None)),
        ('west', sgqlc.types.Arg(sgqlc.types.non_null(Float), graphql_name='west', default=None)),
        ('north', sgqlc.types.Arg(sgqlc.types.non_null(Float), graphql_name='north', default=None)),
        ('south', sgqlc.types.Arg(sgqlc.types.non_null(Float), graphql_name='south', default=None)),
        ('where', sgqlc.types.Arg(MapReportFilter, graphql_name='where', default=None)),
))
    )


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
    __field_names__ = ('answer_value', 'entity', 'value', 'value_bool', 'value_date', 'value_long', 'value_double', 'is_enabled')
    answer_value = sgqlc.types.Field(Int, graphql_name='answerValue')
    entity = sgqlc.types.Field(sgqlc.types.non_null(Entity), graphql_name='entity')
    value = sgqlc.types.Field(String, graphql_name='value')
    value_bool = sgqlc.types.Field(Boolean, graphql_name='valueBool')
    value_date = sgqlc.types.Field(DateTime, graphql_name='valueDate')
    value_long = sgqlc.types.Field(Long, graphql_name='valueLong')
    value_double = sgqlc.types.Field(Float, graphql_name='valueDouble')
    is_enabled = sgqlc.types.Field(Boolean, graphql_name='isEnabled')


class Interview(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('action_flags', 'assignment_id', 'id', 'status', 'interview_mode', 'responsible_name', 'responsible_id', 'responsible_role', 'supervisor_name', 'was_completed', 'created_date', 'key', 'client_key', 'update_date_utc', 'received_by_interviewer_at_utc', 'errors_count', 'questionnaire_id', 'questionnaire_variable', 'questionnaire_version', 'identifying_data', 'not_answered_count', 'calendar_event', 'cawi_link')
    action_flags = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(InterviewActionFlags))), graphql_name='actionFlags')
    assignment_id = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='assignmentId')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    status = sgqlc.types.Field(sgqlc.types.non_null(InterviewStatus), graphql_name='status')
    interview_mode = sgqlc.types.Field(sgqlc.types.non_null(InterviewMode), graphql_name='interviewMode')
    responsible_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='responsibleName')
    responsible_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='responsibleId')
    responsible_role = sgqlc.types.Field(sgqlc.types.non_null(UserRoles), graphql_name='responsibleRole')
    supervisor_name = sgqlc.types.Field(String, graphql_name='supervisorName')
    was_completed = sgqlc.types.Field(sgqlc.types.non_null(Boolean), graphql_name='wasCompleted')
    created_date = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='createdDate')
    key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='key')
    client_key = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='clientKey')
    update_date_utc = sgqlc.types.Field(sgqlc.types.non_null(DateTime), graphql_name='updateDateUtc')
    received_by_interviewer_at_utc = sgqlc.types.Field(DateTime, graphql_name='receivedByInterviewerAtUtc')
    errors_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='errorsCount')
    questionnaire_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='questionnaireId')
    questionnaire_variable = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='questionnaireVariable')
    questionnaire_version = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='questionnaireVersion')
    identifying_data = sgqlc.types.Field(sgqlc.types.list_of(IdentifyingEntity), graphql_name='identifyingData')
    not_answered_count = sgqlc.types.Field(Int, graphql_name='notAnsweredCount')
    calendar_event = sgqlc.types.Field(CalendarEvent, graphql_name='calendarEvent')
    cawi_link = sgqlc.types.Field(String, graphql_name='cawiLink')


class Map(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('file_name', 'size', 'import_date', 'import_date_utc', 'uploaded_by', 'users', 'x_max_val', 'y_max_val', 'x_min_val', 'y_min_val', 'wkid', 'max_scale', 'min_scale', 'shape_type', 'shapes_count')
    file_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='fileName')
    size = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='size')
    import_date = sgqlc.types.Field(DateTime, graphql_name='importDate') # before 21.05
    import_date_utc = sgqlc.types.Field(DateTime, graphql_name='importDateUtc')
    uploaded_by = sgqlc.types.Field(UUID, graphql_name='uploadedBy')
    users = sgqlc.types.Field(sgqlc.types.list_of('UserMap'), graphql_name='users')
    x_max_val = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='xMaxVal')
    y_max_val = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='yMaxVal')
    x_min_val = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='xMinVal')
    y_min_val = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='yMinVal')
    wkid = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='wkid')
    max_scale = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='maxScale')
    min_scale = sgqlc.types.Field(sgqlc.types.non_null(Float), graphql_name='minScale')
    shape_type = sgqlc.types.Field(String, graphql_name='shapeType')
    shapes_count = sgqlc.types.Field(Int, graphql_name='shapesCount')


class MapReport(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('total_point', 'initial_bounds', 'feature_collection')
    total_point = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalPoint')
    initial_bounds = sgqlc.types.Field(GeoBounds, graphql_name='initialBounds')
    feature_collection = sgqlc.types.Field(FeatureCollection, graphql_name='featureCollection')


class MapReportHolder(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('report',)
    report = sgqlc.types.Field(sgqlc.types.non_null(MapReport), graphql_name='report')


class Questionnaire(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('variable', 'questionnaire_id', 'version', 'id', 'title', 'default_language_name', 'translations')
    variable = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='variable')
    questionnaire_id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='questionnaireId')
    version = sgqlc.types.Field(sgqlc.types.non_null(Long), graphql_name='version')
    id = sgqlc.types.Field(ID, graphql_name='id')
    title = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='title')
    default_language_name = sgqlc.types.Field(String, graphql_name='defaultLanguageName')
    translations = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null('Translation'))), graphql_name='translations')


class QuestionnaireItem(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('entity_type', 'title', 'variable', 'scope', 'label', 'type', 'variable_type', 'identifying', 'included_in_reporting_at_utc', 'options')
    entity_type = sgqlc.types.Field(EntityType, graphql_name='entityType')
    title = sgqlc.types.Field(String, graphql_name='title')
    variable = sgqlc.types.Field(String, graphql_name='variable')
    scope = sgqlc.types.Field(QuestionScope, graphql_name='scope')
    label = sgqlc.types.Field(String, graphql_name='label')
    type = sgqlc.types.Field(QuestionType, graphql_name='type')
    variable_type = sgqlc.types.Field(VariableType, graphql_name='variableType')
    identifying = sgqlc.types.Field(Boolean, graphql_name='identifying')
    included_in_reporting_at_utc = sgqlc.types.Field(DateTime, graphql_name='includedInReportingAtUtc')
    options = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(CategoricalOption))), graphql_name='options')


class Translation(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('id', 'name')
    id = sgqlc.types.Field(sgqlc.types.non_null(UUID), graphql_name='id')
    name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='name')


class User(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('id', 'role', 'user_name', 'full_name', 'email', 'phone_number', 'creation_date', 'is_locked', 'is_archived', 'workspaces')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    role = sgqlc.types.Field(sgqlc.types.non_null(UserRoles), graphql_name='role')
    user_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='userName')
    full_name = sgqlc.types.Field(String, graphql_name='fullName')
    email = sgqlc.types.Field(String, graphql_name='email')
    phone_number = sgqlc.types.Field(String, graphql_name='phoneNumber')
    creation_date = sgqlc.types.Field(Date, graphql_name='creationDate')
    is_locked = sgqlc.types.Field(Boolean, graphql_name='isLocked')
    is_archived = sgqlc.types.Field(Boolean, graphql_name='isArchived')
    workspaces = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='workspaces')


class UserMap(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('user_name',)
    user_name = sgqlc.types.Field(String, graphql_name='userName')


class Users(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('nodes', 'total_count', 'filtered_count')
    nodes = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(User)), graphql_name='nodes')
    total_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='totalCount')
    filtered_count = sgqlc.types.Field(sgqlc.types.non_null(Int), graphql_name='filteredCount')


class Viewer(sgqlc.types.Type):
    __schema__ = headquarters_schema
    __field_names__ = ('id', 'role', 'user_name', 'workspaces')
    id = sgqlc.types.Field(sgqlc.types.non_null(ID), graphql_name='id')
    role = sgqlc.types.Field(sgqlc.types.non_null(UserRoles), graphql_name='role')
    user_name = sgqlc.types.Field(sgqlc.types.non_null(String), graphql_name='userName')
    workspaces = sgqlc.types.Field(sgqlc.types.non_null(sgqlc.types.list_of(sgqlc.types.non_null(String))), graphql_name='workspaces')



########################################################################
# Unions
########################################################################

########################################################################
# Schema Entry Points
########################################################################
headquarters_schema.query_type = HeadquartersQuery
headquarters_schema.mutation_type = HeadquartersMutation
headquarters_schema.subscription_type = None

