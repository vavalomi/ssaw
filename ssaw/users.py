from datetime import datetime
from typing import Generator
from uuid import UUID

from sgqlc.operation import Operation

from .base import HQBase
from .headquarters_schema import HeadquartersQuery, UsersFilterInput
from .headquarters_schema import User as GraphQLUser, Viewer
from .models import InterviewerAction, User
from .utils import filter_object, order_object


class UsersApi(HQBase):
    """ Set of functions to access and manipulate Users. """

    _apiprefix = "/api/v1"

    def get_list(self, fields: list = [],
                 order=None, skip: int = None, take: int = None,
                 where: UsersFilterInput = None, **kwargs) -> Generator[GraphQLUser, None, None]:

        q_args = {
        }
        if order:
            q_args["order"] = order_object("UsersSortInput", order)
        if skip:
            q_args["skip"] = skip
        if take:
            q_args["take"] = take
        if where or kwargs:
            q_args['where'] = filter_object("UsersFilterInput", where=where, **kwargs)

        op = Operation(HeadquartersQuery)
        q = op.users(**q_args)
        q.nodes.__fields__(*fields)
        cont = self._make_graphql_call(op)
        res = (op + cont).users

        yield from res.nodes

    def get_info(self, id):
        path = self._url_users + '/{}'.format(id)
        return self._make_call('get', path)

    def get_actions_log(
            self, id: UUID, start: datetime = None, end: datetime = None) -> Generator[InterviewerAction, None, None]:

        path = self._url_interviewers + '/{}/actions-log'.format(id)
        params = {}
        if start:
            params["start"] = start.strftime("%Y-%m-%d")
        if end:
            params["end"] = end.strftime("%Y-%m-%d")
        response = self._make_call('get', path, params=params)
        for ac in response:
            yield InterviewerAction(**ac)

    def list_supervisors(self):
        path = self._url_supervisors
        return self._list_users(path)

    def list_interviewers(self, id):
        path = self._url_supervisors + '/{}/interviewers'.format(id)
        return self._list_users(path)

    def unarchive(self, id):
        path = self._url_users + '/{}/unarchive'.format(id)
        return self._make_call('patch', path)

    def archive(self, id):
        path = self._url_users + '/{}/archive'.format(id)
        return self._make_call('patch', path)

    def create(self, **kwargs):

        user = User(**kwargs)
        path = self._url_users

        return self._make_call("post", path, data=user.json(by_alias=True),
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
        return self.url + '/users'

    @property
    def _url_supervisors(self):
        return self.url + '/supervisors'

    @property
    def _url_interviewers(self):
        return self.url + '/interviewers'
