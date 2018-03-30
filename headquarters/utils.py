class NotFoundError(Exception):
	def __init__(self, objecttype):
		self.expression = objecttype + ' not found'
		self.message = objecttype + ' not found'