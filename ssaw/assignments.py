from .base import HQBase
from .utils import to_qidentity
from .exceptions import NotFoundError
from .models import Assignment

class AssignmentsApi(HQBase):
    _apiprefix = "/api/v1/assignments"

    def get_list(self, questionnaire_id = None, questionnaire_version = None):
        path = self.url
        limit = 10
        offset = 1
        total_count = 11
        params = {
            'offset': offset,
            'limit': limit
        }
        if questionnaire_id and questionnaire_version:
            params['questionnaireId'] = to_qidentity(questionnaire_id, questionnaire_version) 

        while offset < total_count:
            params['offset'] = offset
            r = self._make_call('get', path, params=params)
            total_count = r['TotalCount']
            for item in r['Assignments']:
                yield Assignment.from_dict(item)
            offset += limit

    def get_info(self, id):
        path = self.url + "/{}".format(id)
        item = self._make_call("get", path)
        return Assignment.from_dict(item)

    def create(self, assignment):
        """Calls POST /api/v1/assignments to create new assignment.

        Args:
            assignment: `ssaw.models.Assignment` object
        
        Returns:
            True
        """
        path = self.url
        return self._make_call("post", path, json=assignment.to_json())

    def archive(self, id):
        pass

    def assign(self, id, responsible):
        pass

    def get_quantity_settings(self, id):
        pass

    def update_quantity(self, id, quantity):
        pass

    def close(self, id):
        pass

    def history(self, id):
        pass

    def get_recordaudio(self, id):
        pass

    def update_recordaudio(self, id):
        pass

    def unarchive(self, id):
        pass
