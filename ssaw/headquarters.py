from typing import Optional

from requests import Session

from .__about__ import __title__, __version__
from .models import Version


class Client(object):
    """Initializes the API client

    :param url: URL of the headquarters app
    :param api_user: API user name
    :param api_password: API user password
    :param token: Authorization token
    :param workspace: Name of the workspace. If `None`, "primary" will be assumed
    """

    def __init__(self, url: str,
                 api_user: Optional[str] = None, api_password: Optional[str] = None,
                 token: Optional[str] = None,
                 workspace: str = "primary"):
        session = Session()

        if token:
            session.headers.update({"Authorization": f"Bearer {token}"})
        elif api_user and api_password:
            session.auth = (api_user, api_password)

        signature = f"python-{__title__}/{__version__}"
        session.headers.update({"User-Agent": signature})
        self.baseurl = url.rstrip("/")
        self.session = session
        self.workspace = workspace

    @property
    def version(self) -> Version:
        res = self.session.get(f"{self.baseurl}/.version")
        res.raise_for_status()
        return Version(res.text)
