class Assignments(object):
	def __init__(self, url, session):
		self.url = url + 'assignments'
		self.session = session

	def __call__(self, id=None):
		path = self.url
		if id:
			path = path + '/{}'.format(id)
		response = self.session.get(path)
		return response.json()
