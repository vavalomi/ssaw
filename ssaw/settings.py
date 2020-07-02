from .base import HQBase


class SettingsApi(HQBase):
    _apiprefix = "/api/v1/settings"

    def get_globalnotice(self):
        """GET /api/v1/settings/globalnotice"""

        path = self.url + '/globalnotice'
        r = self._make_call('get', path)
        return str(r['Message'] or '')

    def set_globalnotice(self, message):
        """PUT /api/v1/settings/globalnotice"""

        path = self.url + '/globalnotice'
        self._make_call('put', path, json={'message': message})

    def remove_globalnotice(self):
        """DELETE /api/v1/settings/globalnotice"""

        path = self.url + '/globalnotice'
        self._make_call('delete', path)
