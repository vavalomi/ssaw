import json
import os
import re

from sgqlc.endpoint.requests import RequestsEndpoint

from .exceptions import (
    ForbiddenError, GraphQLError,
    NotAcceptableError, NotFoundError, UnauthorizedError
)
from .headquarters import Client


class HQBase(object):
    _apiprefix: str = ""

    def __init__(self, client: Client, workspace: str = None) -> None:
        self._hq = client
        if workspace:
            self.workspace = workspace
        else:
            self.workspace = client.workspace

    @property
    def url(self) -> str:
        if self.workspace:
            path = '/' + self.workspace + self._apiprefix
        else:
            path = self._apiprefix
        return self._hq.baseurl + path

    def _make_call(self, method: str, path: str, filepath: str = None, parser=None, **kwargs):
        response = self._hq.session.request(method=method, url=path, **kwargs)
        if response.status_code < 300:
            if method == 'get':
                if 'application/json' in response.headers['Content-Type']:
                    if parser:
                        return parser(response.content)
                    else:
                        return json.loads(response.content)

                elif 'application/zip' in response.headers['Content-Type']:
                    return self._get_file_stream(filepath, response)
            else:
                return json.loads(response.content) if response.content else True

        else:
            self._process_status_code(response)

    def _make_graphql_call(self, op):
        endpoint = RequestsEndpoint(self._hq.baseurl + '/graphql', session=self._hq.session)
        cont = endpoint(op)
        errors = cont.get('errors')
        if errors:
            try:
                rc = errors[0]['extensions']['code']
            except KeyError:
                rc = None
            if rc == 'AUTH_NOT_AUTHENTICATED':
                raise UnauthorizedError()
            else:
                raise GraphQLError(errors[0]['message'])
        else:
            return cont

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
            r"filename[ ]*=([^;]+)", d, flags=re.IGNORECASE)

        if not fname:
            fname = re.findall(
                r"filename\*=utf-8''(.+)", d, flags=re.IGNORECASE)

        fname = fname[0].strip().strip('"')
        outfile = os.path.join(filepath, fname)

        with open(outfile, 'wb') as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        return outfile
