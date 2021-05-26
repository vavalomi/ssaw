import json
import os
import re
from urllib.parse import unquote

from requests import Session

from sgqlc.endpoint.requests import RequestsEndpoint
from sgqlc.operation import Operation

from .exceptions import (
    ForbiddenError, GraphQLError,
    NotAcceptableError, NotFoundError, UnauthorizedError
)
from .headquarters import Client
from .headquarters_schema import HeadquartersMutation


class HQBase(object):
    _apiprefix: str = ""

    def __init__(self, client: Client, workspace: str = None) -> None:
        self._hq = client
        self.workspace = workspace or client.workspace

    @property
    def url(self) -> str:
        if self.workspace:
            path = '/' + self.workspace + self._apiprefix
        else:
            path = self._apiprefix
        return self._hq.baseurl + path

    def _make_call(self, method: str, path: str, filepath: str = None, parser=None, use_login_session=False, **kwargs):
        if use_login_session:
            with Session() as login_session:
                response = login_session.request(method="post",
                                                 url=f"{self._hq.baseurl}/Account/LogOn",
                                                 data={"UserName": self._hq.session.auth[0],
                                                       "Password": self._hq.session.auth[1]})
                if response.status_code < 300:
                    response = login_session.request(method=method, url=path, **kwargs)
                else:
                    self._process_status_code(response)

        else:
            response = self._hq.session.request(method=method, url=path, **kwargs)
        if response.status_code < 300:
            if method == 'get':
                if 'application/json' in response.headers['Content-Type']:
                    if parser:
                        return parser(response.content)
                    else:
                        return json.loads(response.content)

                elif ('application/zip' in response.headers['Content-Type']
                      or 'application/octet-stream' in response.headers['Content-Type']):
                    return self._get_file_stream(filepath, response)
            else:
                return json.loads(response.content) if response.content else True

        else:
            self._process_status_code(response)

    def _call_mutation(self, method_name: str, fields: list = [], **kwargs):
        op = Operation(HeadquartersMutation)
        func = getattr(op, method_name)
        kwargs["workspace"] = self.workspace
        func(**kwargs).__fields__(*fields)
        cont = self._make_graphql_call(op)

        res = (op + cont)
        return getattr(res, method_name)

    def _make_graphql_call(self, op, **kwargs):
        if "session" not in kwargs:
            kwargs["session"] = self._hq.session
        endpoint = RequestsEndpoint(self._hq.baseurl + '/graphql', **kwargs)
        cont = endpoint(op)
        errors = cont.get('errors')
        if not errors:
            return cont

        try:
            rc = errors[0]['extensions']['code']
        except KeyError:
            rc = None
        if rc == 'AUTH_NOT_AUTHENTICATED':
            raise UnauthorizedError()
        else:
            raise GraphQLError(errors[0]['message'])

    @staticmethod
    def _process_status_code(response):
        rc = response.status_code
        if rc == 401:
            raise UnauthorizedError()
        elif rc == 403:
            raise ForbiddenError()
        elif rc == 404:
            raise NotFoundError(response.text)
        elif rc in [400, 406]:
            raise NotAcceptableError(response.text)
        else:
            response.raise_for_status()

    @staticmethod
    def _get_file_stream(filepath, response):
        d = response.headers['content-disposition']
        fname = re.findall(
            r"filename\*=utf-8''(.+)", d, flags=re.IGNORECASE)

        if not fname:
            fname = re.findall(
                r"filename[ ]*=([^;]+)", d, flags=re.IGNORECASE)

        fname = fname[0].strip().strip('"')
        outfile = os.path.join(filepath, unquote(fname))

        with open(outfile, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return outfile
