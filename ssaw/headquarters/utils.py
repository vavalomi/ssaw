class NotFoundError(Exception):
	def __init__(self, objecttype):
		self.expression = objecttype + ' not found'
		self.message = objecttype + ' not found'

class IncompleteQuestionnaireIdError(Exception):
	def __init__(self):
		self.expression = 'Invalid questionnaire id'
		self.message = 'Both questionnaire guid and version number must be specified'