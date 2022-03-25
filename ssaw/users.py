from datetime import datetime
from typing import Iterator
from uuid import UUID

from sgqlc.operation import Operation

from .base import HQBase
from .headquarters import Client
from .headquarters_schema import HeadquartersQuery, UsersFilterInput
from .headquarters_schema import User as GraphQLUser, Viewer
from .models import InterviewerAction, User, UserRole
from .utils import filter_object, order_object


class UsersApi(HQBase):
    """ Set of functions to access and manipulate Users. """

    _apiprefix = "/api/v1"

    def __init__(self, client: Client) -> None:
        super().__init__(client)

    def get_list(self, fields: list = None,
                 order=None, skip: int = 0, take: int = None,
                 where: UsersFilterInput = None, **kwargs) -> Iterator[GraphQLUser]:

        if fields is None:
            fields = []
        q_args = {
        }
        if order:
            q_args["order"] = order_object("UsersSortInput", order)
        if where or kwargs:
            q_args['where'] = filter_object("UsersFilterInput", where=where, **kwargs)

        op = self._graphql_query_operation('users', q_args)
        op.users.nodes.__fields__(*fields)

        yield from self._get_full_list(op, 'users', skip=skip, take=take)

    def get_info(self, id):
        return self._make_call(method="get", path=f"{self._url_users}/{id}")

    def get_actions_log(
            self, id: UUID, start: datetime = None, end: datetime = None) -> Iterator[InterviewerAction]:

        params = {}
        if start:
            params["start"] = start.strftime("%Y-%m-%d")
        if end:
            params["end"] = end.strftime("%Y-%m-%d")
        response = self._make_call(method="get",
                                   path=f"{self._url_interviewers}/{id}/actions-log",
                                   params=params)
        for ac in response:
            yield InterviewerAction(**ac)

    def list_supervisors(self):
        path = self._url_supervisors
        return self._list_users(path)

    def list_interviewers(self, id):
        return self._list_users(f"{self._url_supervisors}/{id}/interviewers")

    def unarchive(self, id):
        return self._make_call(method="patch", path=f"{self._url_users}/{id}/unarchive")

    def archive(self, id):
        return self._make_call(method="patch", path=f"{self._url_users}/{id}/archive")

    def create(self, user_name: str, password: str, role: UserRole = UserRole.INTERVIEWER,
               supervisor: str = "", full_name: str = "", email: str = "", phone_number: str = "") -> None:

        user = User(user_name=user_name, password=password, role=role, supervisor=supervisor,
                    full_name=full_name, email=email, phone_number=phone_number)

        return self._make_call(method="post", path=self._url_users,
                               data=user.json(by_alias=True),
                               headers={"content-type": "application/json"})

    def viewer(self, username: str = None, password: str = None) -> Viewer:
        op = Operation(HeadquartersQuery)
        op.viewer()
        if username and password:
            cont = self._make_graphql_call(op, auth=(username, password))
        else:
            cont = self._make_graphql_call(op)

        return (op + cont).viewer

    def _list_users(self, path):
        page_size = 10
        page = 1
        total_count = 11
        params = {
            'offset': page,
            'limit': page_size
        }
        while (page - 1) * page_size < total_count:
            params['offset'] = page
            r = self._make_call('get', path, params=params)
            total_count = r['TotalCount']
            if total_count > 0:
                yield from r['Users']
            else:
                yield from ()
            page += 1

    @property
    def _url_users(self):
        return f"{self.url}/users"

    @property
    def _url_supervisors(self):
        return f"{self.url}/supervisors"

    @property
    def _url_interviewers(self):
        return f"{self.url}/interviewers"
