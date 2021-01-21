
from requests import Session

from .__about__ import __title__, __version__
from .models import Version


class Client(object):
    """Initializes the API client

    Parameters
    ----------
    url: str
        URL of the headquarters app
    api_user: str
        API user name
    api_password: str
        API user password
    """

    def __init__(self, url: str, api_user: str, api_password: str, workspace: str = None):
        session = Session()
        session.auth = (api_user, api_password)
        signature = 'python-{}/{}'.format(__title__, __version__)
        session.headers.update({'User-Agent': signature})
        self.baseurl = url.rstrip("/")
        self.session = session
        self._workspace = workspace

    @property
    def version(self) -> Version:
        res = self.session.get("{}/.version".format(self.baseurl))
        if res.status_code == 200:
            return Version(res.text)

