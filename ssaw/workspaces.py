from typing import List

from .base import HQBase
from .exceptions import FeatureNotSupported
from .headquarters import Client
from .models import Version
from .utils import fix_qid


class WorkspacesApi(HQBase):
    """ Set of functions to access and manipulate Workspaces. """

    _apiprefix = "/api/v1/workspaces"

    def __init__(self, client: Client):
        if client.version < Version("21.01 (build 30293)"):
            raise FeatureNotSupported

        super().__init__(client)

    @fix_qid(expects={'user_id': 'string'})
    def get_list(self, user_id: str = None, include_disabled: bool = False):
        path = self.url
        length = 10
        start = 0
        total_count = 11
        params = {
            'start': start,
            'length': length,
            'IncludeDisabled': include_disabled,
            'UserId': user_id
        }
        while start < total_count:
            params['start'] = start
            r = self._make_call('get', path, params=params)
            if r.get("TotalCount"):
                total_count = r['TotalCount']
                yield from r['Workspaces']
            else:
                yield from ()
            start += length

    def get_info(self, name: str):
        path = self.url + '/{}'.format(name)
        return self._make_call('get', path)

    def create(self, name: str, display_name: str):
        path = self.url
        return self._make_call('post', path, json={'Name': name, 'DisplayName': display_name})

    def update(self, name: str, display_name: str):
        path = self.url + '/{}'.format(name)
        return self._make_call('patch', path, json={'DisplayName': display_name})

    def delete(self, name: str):
        path = self.url + '/{}'.format(name)
        _ = self._make_call('delete', path)

        return True

    def enable(self, name: str):
        path = self.url + '/{}/enable'.format(name)
        return self._make_call('post', path)

    def disable(self, name: str):
        path = self.url + '/{}/disable'.format(name)
        return self._make_call('post', path)

    def assign(self, user_ids: List[str], workspaces: List[str], supervisors: List[str] = None, mode: str = "add"):
        path = self.url + '/assign'

        if not isinstance(user_ids, list):
            user_ids = [user_ids]
        if not isinstance(workspaces, list):
            workspaces = [workspaces]
        if not isinstance(supervisors, list):
            supervisors = [supervisors]
        if mode.lower() not in ["add", "assign", "remove"]:
            raise ValueError("mode parameter must be one of 'add', 'assign', or 'remove'")

        data = {
            "UserIds": user_ids,
            "Workspaces": [{"workspace": w, "supervisorId": s} for w, s in zip(workspaces, supervisors)],
            "Mode": mode
        }
        return self._make_call('post', path, json=data)

    def status(self, name: str):
        path = self.url + '/status/{}'.format(name)
        return self._make_call('get', path)
