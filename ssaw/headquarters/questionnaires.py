from .utils import IncompleteQuestionnaireIdError

class Questionnaires(object):
	def __init__(self, url, session):
		self.url = url + 'questionnaires'
		self.session = session

	def __call__(self, id=None, version=None):
		path = self.url
		if id and version:
			path = path + '/{}/{}'.format(id, version)
		else:
			if id or version:
				raise IncompleteQuestionnaireIdError()

		response = self.session.get(path)
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