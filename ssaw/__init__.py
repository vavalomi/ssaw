import requests
from .assignments import Assignments
from .export import Export
from .interviews import Interviews
from .utils import *

class ApiObject(object):
	def __init__(self, url, session):
		self.url = url + '/api/v1/'
		self.session = session
		self._assignments = Assignments(self.url, self.session)
		self.Export = Export(self.url, self.session)
		self.Interviews = Interviews(self.url, self.session)

	def Assignments(self, id=None):
		if id:
			return self._assignments.GetOne(id)
		else:
			return self._assignments.GetList()

def init(url, api_user, api_password):
	session = requests.Session()
	session.auth = (api_user, api_password)
	return ApiObject(url, session)