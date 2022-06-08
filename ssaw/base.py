import os
import re
from typing import Dict, List, Optional, Union
from urllib.parse import unquote

from requests import Response, Session

from sgqlc.endpoint.requests import RequestsEndpoint
from sgqlc.operation import Operation
from sgqlc.types import Arg, Int, Variable

from .exceptions import ForbiddenError, GraphQLError, NotAcceptableError, NotFoundError, UnauthorizedError
from .headquarters import Client
from .headquarters_schema import HeadquartersMutation, HeadquartersQuery


GRAPHQL_PAGE_SIZE = 100


class HQBase(object):
    _apiprefix: str = "/"

    def __init__(self, client: Client, workspace: Optional[str] = None) -> None:
        self._hq = client
        self.workspace = client.workspace if workspace is None else workspace

    @property
    def url(self) -> str:
        return (f"{self._hq.baseurl}/{self.workspace}{self._apiprefix}" if self.workspace else
                f"{self._hq.baseurl}{self._apiprefix}")

    def _make_call(self, method: str, path: str, filepath: Optional[str] = None,
                   use_login_session: bool = False, **kwargs) -> Union[Dict[str, dict], str, None]:

        if use_login_session:
            response = self._make_call_with_login(method=method, path=path, **kwargs)
        else:
            response = self._hq.session.request(method=method, url=path, **kwargs)

        self._process_status_code(response)

        if 'Content-Type' in response.headers:
            if 'application/json' in response.headers['Content-Type']:
                return response.json()

            elif any(w in response.headers['Content-Type'] for w in ['application/zip', 'application/octet-stream']):
                return self._get_file_stream(filepath, response)
            else:
                return response.text

    def _make_call_with_login(self, method: str, path: str, **kwargs) -> Response:
        if self._hq.session.auth is None:
            raise UnauthorizedError

        url = f"{self._hq.baseurl}/Account/LogOn"
        with Session() as login_session:
            login_session.headers.update({"User-Agent": self._hq.session.headers["User-Agent"]})
            response = login_session.request(method="post",
                                             url=url,
                                             data={"UserName": self._hq.session.auth[0],
                                                   "Password": self._hq.session.auth[1]})
            self._process_status_code(response)
            if response.url == url:
                raise UnauthorizedError()

            # navigate to the page first to retrieve the CSRF token
            _ = login_session.request(method="get", url=path)
            if "CSRF-TOKEN" in login_session.cookies:
                login_session.headers.update({"X-CSRF-TOKEN": login_session.cookies["CSRF-TOKEN"]})

            return login_session.request(method=method, url=path, **kwargs)

    def _call_mutation(self, method_name: str, fields: Optional[List[str]] = None, **kwargs):
        if fields is None:
            fields = []
        op = Operation(HeadquartersMutation)
        func = getattr(op, method_name)
        kwargs["workspace"] = self.workspace
        func(**kwargs).__fields__(*fields)
        cont = self._make_graphql_call(op)

        res = (op + cont)
        return getattr(res, method_name)

    @staticmethod
    def _graphql_query_operation(selector_name: str, args: dict):
        op = Operation(HeadquartersQuery, variables={'take': Arg(Int), 'skip': Arg(Int), })
        getattr(op, selector_name)(take=Variable('take'), skip=Variable('skip'), **args)

        return op

    def _get_full_list(self, op: Operation, selector_name: str, skip: int = 0, take: Optional[int] = None):
        query = bytes(op).decode('utf-8')

        returned_count = 0
        local_take = returned_count + GRAPHQL_PAGE_SIZE if take is None else take
        while returned_count < local_take:
            page_size = min(GRAPHQL_PAGE_SIZE, local_take - returned_count)
            cont = self._make_graphql_call(query, variables={'take': page_size, 'skip': skip + returned_count})
            res = getattr((op + cont), selector_name).nodes
            max_index = min(len(res), local_take - returned_count)
            if max_index == 0:
                return
            yield from res[:max_index]
            returned_count += page_size
            local_take = returned_count + GRAPHQL_PAGE_SIZE if take is None else take

    def _make_graphql_call(self, query, variables: Optional[dict] = None, **kwargs):

        if "session" not in kwargs:
            kwargs["session"] = self._hq.session
        endpoint = RequestsEndpoint(f"{self._hq.baseurl}/graphql", **kwargs)
        cont = endpoint(query, variables=variables)

        errors = cont.get("errors")
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
    def _get_file_stream(filepath, response) -> str:
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
