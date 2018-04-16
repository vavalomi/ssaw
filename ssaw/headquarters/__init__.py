import requests
from .assignments import Assignments
from .export import Export
from .interviews import Interviews
from .questionnaires import Questionnaires
from .users import Users
from .utils import *

class ApiObject(object):
	def __init__(self, url, session):
		self.url = url + '/api/v1/'
		self.session = session
		self.Assignments = Assignments(self.url, self.session)
		self.Export = Export(self.url, self.session)
		self.Interviews = Interviews(self.url, self.session)
		self.Questionnaires = Questionnaires(self.url, self.session)
		self.Users = Users(self.url, self.session)

def init(url, api_user, api_password):
	session = requests.Session()
	session.auth = (api_user, api_password)
	return ApiObject(url, session)