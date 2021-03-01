
from requests import Session

from .__about__ import __title__, __version__
from .models import Version


class Client(object):
    """Initializes the API client

    :param url: URL of the headquarters app
    :param api_user: API user name
    :param api_password: API user password
    :param workspace: Name of the workspace. If `None`, "primary" will be assumed
    """

    def __init__(self, url: str, api_user: str, api_password: str, workspace: str = "primary"):
        session = Session()
        session.auth = (api_user, api_password)
        signature = "python-{}/{}".format(__title__, __version__)
        session.headers.update({"User-Agent": signature})
        self.baseurl = url.rstrip("/")
        self.session = session
        self.workspace = workspace

    @property
    def version(self) -> Version:
        res = self.session.get("{}/.version".format(self.baseurl))
        if res.status_code == 200:
            return Version(res.text)
