
from .base import HQBase
from .exceptions import NotFoundError

class Export(HQBase):
    @property
    def url(self):
        return self._baseurl + '/export'

    def get(self, id, exportpath='', exporttype='Tabular', generate=False):
        """Downloads export file.

        :param id: Questionnaire id in format QuestionnaireGuid$Version
        :param exportpath: Path to save the downloaded file
        :param exporttype: Format of the export data: ``Tabular``, ``STATA``, ``SPSS``, ``Binary``, ``DDI``, ``Paradata``
        :param generate: `True` to trigger new file generation
        :type generate: bool, optional
        """

        response = self.get_info(id, exporttype)
        if response['HasExportedFile'] == True:
            path = self.url + '/{}/{}'.format(exporttype, id)
            return self._make_call('get', path, filepath=exportpath, stream=True)

    def get_info(self, id, exporttype='Tabular'):
        path = self.url + '/{}/{}'.format(exporttype, id) + '/details'
        return self._make_call('get', path)

    def start(self, id, exporttype='Tabular'):
        status = 0
        response = self.get_info(id, exporttype)
        if response['ExportStatus'] == 'NotStarted':
            path = self.url + '/{}/{}'.format(exporttype, id) + '/start'
            status = self._make_call('post', path)
        else:
            print('Export is currently running')

        return status

    def cancel(self, id, exporttype='Tabular'):
        status = 0
        response = self.get_info(id, exporttype)
        if response['ExportStatus'] != 'NotStarted':
            path = self.url + '/{}/{}'.format(exporttype, id) + '/cancel'
            status = self._make_call('post', path)
        else:
            print('No running export process was found')

        return status
