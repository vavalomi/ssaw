from .base import HQBase
from .exceptions import NotFoundError

class Users(HQBase):
    def get_info(self, id):
        path = self._url_users + '/{}'.format(id)
        return self._make_call('get', path)

    def get_actions_log(self, id):
        path = self._url_interviewers + '/{}/actions-log'.format(id)
        return self._make_call('get', path)

    def list_supervisors(self):
        path = self._url_supervisors
        return self._make_call('get', path)

    def list_interviewers(self, id):
        path = self._url_supervisors + '/{}/interviewers'.format(id)
        return self._make_call('get', path)

    def unarchive(self, id):
        path = self._url_users + '/{}/unarchive'.format(id)
        response = self._make_call('patch', path)
        return response

    def archive(self, id):
        path = self._url_users + '/{}/archive'.format(id)
        response = self._make_call('patch', path)
        return response

    @property
    def _url_users(self):
        return self.url + '/users'

    @property
    def _url_supervisors(self):
        return self.url + '/supervisors'

    @property
    def _url_interviewers(self):
        return self.url + '/interviewers'