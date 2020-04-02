import requests
from .assignments import Assignments
from .export import Export
from .interviews import Interviews
from .questionnaires import Questionnaires
from .users import Users
from .settings import Settings

class Headquarters(object):
    """Initializes the API client.

    Args:
        url: URL of the headquarters app
        api_user: API user name
        api_password: API user password
    """

    def __init__(self, url: str, api_user: str, api_password: str):
        session = requests.Session()
        session.auth = (api_user, api_password)
        self.url = url + '/api/v1/'
        self.session = session
        self.assignments = Assignments(self)
        self.export = Export(self)
        self.interviews = Interviews(self)
        self.questionnaires = Questionnaires(self)
        self.users = Users(self)
        self.settings = Settings(self)
