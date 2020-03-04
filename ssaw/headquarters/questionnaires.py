from .base import HQBase
from .exceptions import IncompleteQuestionnaireIdError

class Questionnaires(HQBase):

    @property
    def url(self):
        return self._baseurl + '/questionnaires'

    def __call__(self, id=None, version=None):
        path = self.url
        if id and version:
            path = path + '/{}/{}'.format(id, version)
        else:
            if id or version:
                raise IncompleteQuestionnaireIdError()
        return self._make_call('get', path)

    def statuses(self):
        path = self.url + '/statuses'
        return self._make_call('get', path)

    def document(self, id, version):
        path = self.url + '/{}/{}/document'.format(id, version)
        return self._make_call('get', path)

    def interviews(self, id, version):
        path = self.url + '/{}/{}/interviews'.format(id, version)
        return self._make_call('get', path)

    def update_recordaudio(self, id, version):
        """POST /api/v1/questionnaires/{id}/{version}/recordAudio"""
        pass
