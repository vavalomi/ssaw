class Assignments(object):
	def __init__(self, url, session):
		self.url = url + 'assignments'
		self.session = session

	def GetOne(self, id):
		path = self.url + '/{}'.format(id)
		response = self.session.get(path)
		return response.json()

	def GetList(self):
		response = self.session.get(self.url)
		return response.json()