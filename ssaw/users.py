from .utils import NotFoundError

class Users(object):
	def __init__(self, url, session):
		self.url = url
		self.session = session

	def GetInfo(self, id):
		path = self._url_users() + '/{}'.format(id)
		response = self.session.get(path)
		if response.status_code == 200:
			return response.json()
		else:
			print(response.status_code)
			raise NotFoundError('Id')

	def AllSupervisors(self):
		path = self._url_supervisors()
		response = self.session.get(path)
		return response.json()

	def AllInterviewers(self, id):
		path = self._url_supervisors() + '/{}/interviewers'.format(id)
		response = self.session.get(path)
		return response.json()

	def Unarchive(self, id):
		path = self._url_users() + '/{}/archive'.format(id)
		response = self.session.patch(path)
		return response.status_code

	def Archive(self, id):
		path = self._url_users() + '/{}/unarchive'.format(id)
		response = self.session.patch(path)
		return response.status_code

	def _url_users(self):
		return self.url + '/users'

	def _url_supervisors(self):
		return self.url + '/supervisors'