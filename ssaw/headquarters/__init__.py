import requests
from .assignments import Assignments
from .export import Export
from .interviews import Interviews
from .questionnaires import Questionnaires
from .users import Users
from .settings import Settings

class Headquarters(object):
    """Initializes the API client.

    :param url: URL of the headquarters app
    :param api_user: API user name
    :param api_password: API user password
    :return: :class:`Headquarters <Headquarters>` object
    :rtype: ssaw.Headquarters
    """

    def __init__(self, url, api_user, api_password):
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
