from typing import Iterator

from sgqlc.operation import Operation

from .base import HQBase
from .headquarters_schema import (
    Assignment as GraphQLAssignment,
    AssignmentsFilter,
    CalendarEvent,
    HeadquartersQuery
)
from .models import Assignment, AssignmentHistoryItem
from .utils import filter_object, to_qidentity


class AssignmentsApi(HQBase):
    """ Set of functions to access and manipulate Assignments. """
    _apiprefix = "/api/v1/assignments"

    def get_list(self, questionnaire_id: str = None, questionnaire_version: int = None) -> Iterator[Assignment]:
        """Get list of assignments

        :param questionnaire_id: Filter by specific questionnaire id
        :param questionnaire_version: Filter by specific version number

        :returns: list of :class:`Assignment<ssaw.models.Assignment>` objects
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

    def _get_list(self, fields: list = [], skip: int = None, take: int = None,
                  where: AssignmentsFilter = None, include_calendar_events: bool = False, **kwargs
                  ) -> Iterator[GraphQLAssignment]:

        args = {
            "workspace": self.workspace
        }
        if skip:
            args["skip"] = skip
        if take:
            args["take"] = take

        if where or kwargs:
            args['where'] = filter_object("AssignmentsFilter", where=where, **kwargs)

        op = Operation(HeadquartersQuery)
        q = op.assignments(**args)
        q.nodes.__fields__(*fields)
        if include_calendar_events:
            if type(include_calendar_events) in [list, tuple]:
                q.nodes.calendar_event.__fields__(*include_calendar_events)
            else:
                q.nodes.calendar_event.__fields__()
        cont = self._make_graphql_call(op)
        res = (op + cont).assignments

        yield from res.nodes

    def get_info(self, id: int) -> Assignment:
        """Get single assignment details

        :param id: Assignment Id

        :returns: Assignment object
        """
        path = self.url + "/{}".format(id)
        item = self._make_call("get", path)
        return Assignment.from_dict(item)

    def create(self, obj: Assignment) -> Assignment:
        """Create new assignment

        :param obj: Assignment object to be created

        :returns: Newly created Assignment object
        """
        path = self.url
        res = self._make_call("post", path, json=obj.to_json())
        return Assignment.from_dict(res['Assignment'])

    def archive(self, id: int) -> None:
        """Archive assignment

        :param id: Assignment Id
        """
        path = self.url + "/{}/archive".format(id)
        self._make_call("patch", path)

    def unarchive(self, id: int) -> None:
        """Unarchive assignment

        :param id: Assignment Id
        """
        path = self.url + "/{}/unarchive".format(id)
        self._make_call("patch", path)

    def assign(self, id: int, responsible: str) -> Assignment:
        """Assign new responsible person for assignment

        :param id: Assignment Id
        :param responsible: Username of the new responsible

        :returns: Modified Assignment object
        """
        path = self.url + "/{}/assign".format(id)
        res = self._make_call("patch", path, json={"Responsible": responsible})
        return Assignment.from_dict(res)

    def get_quantity_settings(self, id: int) -> bool:
        """Checi if quantity may be edited for the assignment

        :param id: Assignment Id

        :returns: `True` if quantity can be edited, `False` otherwise
        """
        path = self.url + "/{}/assignmentQuantitySettings".format(id)
        res = self._make_call("get", path)
        return res['CanChangeQuantity']

    def update_quantity(self, id: int, quantity: int) -> Assignment:
        """Change maximum quantity of interviews to be created

        :param id: Assignment Id
        :param quantity: new quantity of interviews to be collected

        :returns: Modified Assignment object

        """
        if not isinstance(quantity, int):
            raise TypeError('quantity must be a number')
        path = self.url + "/{}/changequantity".format(id)
        headers = {"Content-Type": "application/json-patch+json"}
        res = self._make_call("patch", path, data=str(quantity), headers=headers)
        return Assignment.from_dict(res)

    def close(self, id: int) -> None:
        """Close assignment by setting Size to the number of collected interviews

        :param id: Assignment Id
        """
        path = self.url + "/{}/close".format(id)
        self._make_call("post", path)

    def get_history(self, id: int) -> Iterator[dict]:
        page_size = 10
        start = 0
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
            for item in r['History']:
                print(item)
                yield AssignmentHistoryItem(**item)

    def get_recordaudio(self, id: int) -> bool:
        """Get status of audio recording for the assignment

        :param id: Assignment Id

        :returns: `True` if audio recording is enabled, `False` otherwise
        """
        path = self.url + "/{}/recordAudio".format(id)
        res = self._make_call("get", path)
        return res['Enabled']

    def update_recordaudio(self, id: int, enabled: bool) -> None:
        """Turn recording of audio for the assignment

        :param id: Assignment Id
        :param enabled: `True` to turn audio recording on, `False` to turn it off
        """
        if not isinstance(enabled, bool):
            raise TypeError('enabled must be either True or False')
        path = self.url + "/{}/recordAudio".format(id)
        self._make_call("patch", path, json={'Enabled': enabled})

    def get_calendar_event(self, id: int) -> CalendarEvent:
        """Get calendar event associated with the assignment
        """
        assignment = self._get_assignment_by_id(fields=["id"], id=id, include_calendar_events=True)

        return assignment.calendar_event

    def set_calendar_event(self, id: int, new_start: str,
                           start_timezone: str, comment: str = None) -> CalendarEvent:
        """Add new calendar event to the assignment, or update the existing one

        :param id: assignment id to update
        :param new_start: start date of the calendar event
        :param start_timezone: timezone string for the start date
        :param comment: add comment to the calendar event

        :returns: :class:`CalendarEvent' object
        """
        assignment = self._get_assignment_by_id(fields=["id"], id=id, include_calendar_events=["public_key"])

        kwargs = {
            "new_start": new_start,
            "start_timezone": start_timezone,
            "comment": comment
        }
        if hasattr(assignment.calendar_event, "public_key"):
            kwargs["method_name"] = "update_calendar_event"
            kwargs["public_key"] = assignment.calendar_event.public_key
        else:
            kwargs["method_name"] = "add_assignment_calendar_event"
            kwargs["assignment_id"] = assignment.id

        return self._call_mutation(**kwargs)

    def delete_calendar_event(self, id: int) -> CalendarEvent:
        """Remove calendar event associated with the assignment
        """
        assignment = self._get_assignment_by_id(fields=["id"], id=id, include_calendar_events=["public_key"])

        if hasattr(assignment.calendar_event, "public_key"):
            return self._call_mutation(method_name="delete_calendar_event",
                                       public_key=assignment.calendar_event.public_key)

    def _get_assignment_by_id(self, **kwargs):
        # expecting fields, id, include_calendar_events
        try:
            return next(self._get_list(**kwargs))
        except StopIteration:
            raise ValueError("assignment was not found")
