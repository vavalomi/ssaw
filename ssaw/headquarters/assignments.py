from .base import HQBase
from .exceptions import NotFoundError


class Assignments(HQBase):
    """Assignments-related calls.

    """
    @property
    def _url(self):
        return self._baseurl + "/assignments"

    def __call__(self):
        """GET /api/v1/assignments

        Get list of all assignments.
        """

        path = self._url
        return self._make_call("get", path)

    def create(self, assignment):
        """Calls POST /api/v1/assignments to create new assignment.

        Args:
            assignment: `ssaw.models.Assignment` object
        
        Returns:
            True
        """
        path = self._url
        return self._make_call("post", path, data=assignment.to_json())

    def get_info(self, id):
        path = self._url + "/{}".format(id)
        return self._make_call("get", path)

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
