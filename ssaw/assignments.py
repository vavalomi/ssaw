from typing import Iterator

from .base import HQBase
from .models import Assignment
from .utils import to_qidentity


class AssignmentsApi(HQBase):
    _apiprefix = "/api/v1/assignments"

    def get_list(self, questionnaire_id: str = None, questionnaire_version: int = None) -> Iterator[Assignment]:
        """Get list of assignments

        Parameters
        ----------
        questionnaire_id : str, optional
            Filter by specific questionnaire id
        questionnaire_version : int, optional
            Filter by specific version number

        Yields
        -------
        list of :class:`ssaw.models.Assignment` objects
        """
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
            offset += limit
            for item in r['Assignments']:
                yield Assignment.from_dict(item)

    def get_info(self, id: int) -> Assignment:
        """Get single assignment details

        Parameters
        ----------
        id : int
            Assignment Id

        Returns
        -------
            :class:`ssaw.models.Assignment` object
        """
        path = self.url + "/{}".format(id)
        item = self._make_call("get", path)
        return Assignment.from_dict(item)

    def create(self, obj: Assignment) -> Assignment:
        """Create new assignment

        Parameters
        ----------
        obj : Assignment
            Assignment object to be created

        Returns
        -------
            :class:`ssaw.models.Assignment` object
        """
        path = self.url
        res = self._make_call("post", path, json=obj.to_json())
        return Assignment.from_dict(res['Assignment'])

    def archive(self, id: int):
        """Archive assignment

        Parameters
        ----------
        id : int
            Assignment Id
        """
        path = self.url + "/{}/archive".format(id)
        self._make_call("patch", path)

    def unarchive(self, id: int):
        """Unarchive assignment

        Parameters
        ----------
        id : int
            Assignment Id
        """
        path = self.url + "/{}/unarchive".format(id)
        self._make_call("patch", path)

    def assign(self, id: int, responsible: str) -> Assignment:
        """Assign new responsible person for assignment

        Parameters
        ----------
        id : int
            Assignment Id
        responsible : str
            Username of the new responsible

        Returns
        -------
            Modified :class:`ssaw.models.Assignment` object
        """
        path = self.url + "/{}/assign".format(id)
        res = self._make_call("patch", path, json={"Responsible": responsible})
        return Assignment.from_dict(res)

    def get_quantity_settings(self, id: int) -> bool:
        """Checi if quantity may be edited for the assignment

        Parameters
        ----------
        id : int
            Assignment Id

        Returns
        -------
        bool
            `True` if quantity can be edited, `False` otherwise
        """
        path = self.url + "/{}/assignmentQuantitySettings".format(id)
        res = self._make_call("get", path)
        return res['CanChangeQuantity']

    def update_quantity(self, id: int, quantity: int) -> Assignment:
        """Change maximum quantity of interviews to be created

        Parameters
        ----------
        id : int
            Assignment Id
        quantity : int
            new quantity of interviews to be collected

        Returns
        -------
            Modified :class:`ssaw.models.Assignment` object

        """
        if not isinstance(quantity, int):
            raise TypeError('quantity must be a number')
        path = self.url + "/{}/changequantity".format(id)
        headers = {"Content-Type": "application/json-patch+json"}
        res = self._make_call("patch", path, data=str(quantity), headers=headers)
        return Assignment.from_dict(res)

    def close(self, id: int):
        """Close assignment by setting Size to the number of collected interviews

        Parameters
        ----------
        id : int
            Assignment Id
        """
        path = self.url + "/{}/close".format(id)
        self._make_call("post", path)

    def get_history(self, id: int) -> Iterator[dict]:
        page_size = 10
        start = 1
        total_count = 11
        params = {
            'start': start,
            'length': page_size
        }
        path = self.url + "/{}/history".format(id)
        while start < total_count:
            params['start'] = start
            r = self._make_call('get', path, params=params)
            total_count = r['RecordsFiltered']
            start += page_size
            yield from r['History']

    def get_recordaudio(self, id: int) -> bool:
        """Get status of audio recording for the assignment

        Parameters
        ----------
        id : int
            Assignment Id

        Returns
        -------
        bool
            True if audio recording is enabled, False otherwise
        """
        path = self.url + "/{}/recordAudio".format(id)
        res = self._make_call("get", path)
        return res['Enabled']

    def update_recordaudio(self, id: int, enabled: bool):
        """Turn recording of audio for the assignment

        Parameters
        ----------
        id : int
            Assignment Id
        enabled : bool
            True to turn audio recording on, False to turn it off
        """
        if not isinstance(enabled, bool):
            raise TypeError('enabled must be either True or False')
        path = self.url + "/{}/recordAudio".format(id)
        self._make_call("patch", path, json={'Enabled': enabled})
