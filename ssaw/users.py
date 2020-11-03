from datetime import datetime
from typing import Generator
from uuid import UUID

from .base import HQBase
from .models import InterviewerAction


class UsersApi(HQBase):
    _apiprefix = "/api/v1"

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

    def _list_users(self, path):
        page_size = 10
        page = 1
        total_count = 11
        params = {
            'offset': page,
            'limit': page_size
        }
        while page * page_size < total_count:
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
