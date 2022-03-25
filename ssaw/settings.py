from .base import HQBase


class SettingsApi(HQBase):
    """ Set of functions to access and modify Global Notice. """

    _apiprefix = "/api/v1/settings"

    def get_globalnotice(self):
        """GET /api/v1/settings/globalnotice"""

        r = self._make_call('get', self._route_globalnotice)
        return str(r['Message'] or '')

    def set_globalnotice(self, message):
        """PUT /api/v1/settings/globalnotice"""

        self._make_call('put', self._route_globalnotice, json={'message': message})

    def remove_globalnotice(self):
        """DELETE /api/v1/settings/globalnotice"""

        self._make_call('delete', self._route_globalnotice)

    @property
    def _route_globalnotice(self):
        return f"{self.url}/globalnotice"
