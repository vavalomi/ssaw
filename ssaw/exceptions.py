class NotFoundError(Exception):
    def __init__(self, objecttype):
        self.expression = objecttype + ' not found'
        self.message = objecttype + ' not found'


class IncompleteQuestionnaireIdError(Exception):
    def __init__(self):
        self.expression = 'Invalid questionnaire id'
        self.message = 'Both questionnaire guid and version number must be specified'


class UnauthorizedError(Exception):
    def __init__(self):
        self.expression = 'Unauthorized'
        self.message = 'Either username or password were not provided or wrong'


class NotAcceptableError(Exception):
    def __init__(self, message):
        self.expression = 'Not Acceptable'
        self.message = message


class GraphQLError(Exception):
    def __init__(self, message):
        self.expression = 'GraphQL Error'
        self.message = message
