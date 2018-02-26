class Questionnaires(object):
	def __init__(self, url, session):
		self.url = url + 'questionnaires'
		self.session = session

	def GetOne(self, id, version):
		path = self.url + '/{}/{}'.format(id, version)
		response = self.session.get(path)
		return response.json()

	def All(self):
		response = self.session.get(self.url)
		return response.json()

	def Statuses(self):
		path = self.url + '/statuses'
		response = self.session.get(path)
		return response.json()

	def Document(self, id, version):
		path = self.url + '/{}/{}/document'.format(id, version)
		response = self.session.get(path)
		return response.json()

	def Interviews(self, id, version):
		path = self.url + '/{}/{}/interviews'.format(id, version)
		response = self.session.get(path)
		return response.json()