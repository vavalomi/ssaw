from typing import List

from .base import HQBase
from .exceptions import FeatureNotSupported
from .headquarters import Client
from .models import Version


class WorkspacesApi(HQBase):
    """ Set of functions to access and manipulate Workspaces. """

    _apiprefix = "/api/v1/workspaces"

    def __init__(self, client: Client):
        if client.version < Version("21.01 (build 30293)"):
            raise FeatureNotSupported

        super().__init__(client)

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
            if 'TotalCount' in r:
                total_count = r['TotalCount']
                for item in r['Workspaces']:
                    yield item
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
        res = self._make_call('delete', path)
        if 'Success' in res.keys():
            return res['Success']
        else:
            return False

    def enable(self, name: str):
        path = self.url + '/{}/enable'.format(name)
        return self._make_call('post', path)

    def disable(self, name: str):
        path = self.url + '/{}/disable'.format(name)
        return self._make_call('post', path)

    def assign(self, user_ids: List[str], workspaces: List[str]):
        path = self.url + '/assign'
        if not isinstance(user_ids, list):
            user_ids = [user_ids]
        if not isinstance(workspaces, list):
            workspaces = [workspaces]
        data = {
            'UserIds': user_ids,
            'Workspaces': workspaces,
            'Mode': 'Assign'
        }
        return self._make_call('post', path, json=data)

    def status(self, name: str):
        path = self.url + '/status/{}'.format(name)
        return self._make_call('get', path)
