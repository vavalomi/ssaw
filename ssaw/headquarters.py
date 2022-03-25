
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
        signature = f"python-{__title__}/{__version__}"
        session.headers.update({"User-Agent": signature})
        self.baseurl = url.rstrip("/")
        self.session = session
        self.workspace = workspace

    @property
    def version(self) -> Version:
        res = self.session.get(f"{self.baseurl}/.version")
        if res.status_code == 200:
            return Version(res.text)
