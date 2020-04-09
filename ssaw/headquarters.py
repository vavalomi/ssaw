from requests import Session


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

    def __init__(self, url: str, api_user: str, api_password: str):
        session = Session()
        session.auth = (api_user, api_password)
        self.baseurl = url.rstrip("/")
        self.session = session
