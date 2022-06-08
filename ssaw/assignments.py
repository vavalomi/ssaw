from typing import Iterator, List, Optional, Union

from sgqlc.operation import Operation

from .base import HQBase
from .headquarters_schema import (
    Assignment as GraphQLAssignment,
    AssignmentsFilter,
    CalendarEvent,
    HeadquartersQuery,
)
from .models import (
    Assignment,
    AssignmentHistoryItem,
    AssignmentList,
    AssignmentResult,
)
from .utils import filter_object, to_qidentity


class AssignmentsApi(HQBase):
    """ Set of functions to access and manipulate Assignments. """
    _apiprefix = "/api/v1/assignments"

    def get_list(self, questionnaire_id: Optional[str] = None,
                 questionnaire_version: Optional[int] = None) -> Iterator[AssignmentResult]:
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
            'limit': limit,
            'questionnaireId': None,
        }
        if questionnaire_id and questionnaire_version:
            params['questionnaireId'] = to_qidentity(questionnaire_id, questionnaire_version)

        while offset < total_count:
            params['offset'] = offset
            r = AssignmentList.parse_obj(self._make_call('get', path, params=params))
            total_count = r.total_count
            offset += limit
            yield from r.assignments

    def _get_list(self, fields: Optional[List[str]] = None, skip: Optional[int] = None, take: Optional[int] = None,
                  where: Optional[AssignmentsFilter] = None, include_calendar_events: Union[list, tuple, bool] = False,
                  **kwargs) -> Iterator[GraphQLAssignment]:

        if fields is None:
            fields = []
        args = {
            "workspace": self.workspace,
            "skip": None,
            "take": None,
        }
        if skip:
            args["skip"] = skip
        if take:
            args["take"] = take

        if where or kwargs:
            args['where'] = filter_object(AssignmentsFilter, where=where, **kwargs)

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

    def get_info(self, id: int) -> AssignmentResult:
        """Get single assignment details

        :param id: Assignment Id

        :returns: Assignment object
        """
        return AssignmentResult.parse_obj(self._make_call(method="get", path=f"{self.url}/{id}"))

    def create(self, obj: Assignment) -> AssignmentResult:
        """Create new assignment

        :param obj: Assignment object to be created

        :returns: Newly created Assignment object
        """
        res = self._make_call(method="post", path=self.url, json=obj.dict(by_alias=True, exclude_none=True))
        return AssignmentResult.parse_obj(res["Assignment"])

    def archive(self, id: int) -> None:
        """Archive assignment

        :param id: Assignment Id
        """
        self._make_call(method="patch", path=f"{self.url}/{id}/archive")

    def unarchive(self, id: int) -> None:
        """Unarchive assignment

        :param id: Assignment Id
        """
        self._make_call(method="patch", path=f"{self.url}/{id}/unarchive")

    def assign(self, id: int, responsible: str) -> AssignmentResult:
        """Assign new responsible person for assignment

        :param id: Assignment Id
        :param responsible: Username of the new responsible

        :returns: Modified Assignment object
        """
        res = self._make_call(method="patch",
                              path=f"{self.url}/{id}/assign",
                              json={"Responsible": responsible})
        return AssignmentResult.parse_obj(res)

    def get_quantity_settings(self, id: int) -> bool:
        """Checi if quantity may be edited for the assignment

        :param id: Assignment Id

        :returns: `True` if quantity can be edited, `False` otherwise
        """
        res = self._make_call(method="get",
                              path=f"{self.url}/{id}/assignmentQuantitySettings")
        return res['CanChangeQuantity']

    def update_quantity(self, id: int, quantity: int) -> AssignmentResult:
        """Change maximum quantity of interviews to be created

        :param id: Assignment Id
        :param quantity: new quantity of interviews to be collected

        :returns: Modified Assignment object

        """
        if not isinstance(quantity, int):
            raise TypeError('quantity must be a number')

        res = self._make_call(method="patch",
                              path=f"{self.url}/{id}/changequantity",
                              data=str(quantity),
                              headers={"Content-Type": "application/json-patch+json"})
        return AssignmentResult.parse_obj(res)

    def close(self, id: int) -> None:
        """Close assignment by setting Size to the number of collected interviews

        :param id: Assignment Id
        """
        self._make_call(method="post", path=f"{self.url}/{id}/close".format(id))

    def get_history(self, id: int) -> Iterator[dict]:
        page_size = 10
        start = 0
        total_count: int = 11
        params = {
            'length': page_size,
        }
        path = f"{self.url}/{id}/history"
        while start < total_count:
            params['start'] = start
            r = self._make_call('get', path, params=params)
            total_count = r['RecordsFiltered']
            start += page_size
            for item in r['History']:
                yield AssignmentHistoryItem.parse_obj(item)

    def get_recordaudio(self, id: int) -> bool:
        """Get status of audio recording for the assignment

        :param id: Assignment Id

        :returns: `True` if audio recording is enabled, `False` otherwise
        """
        res = self._make_call(method="get", path=f"{self.url}/{id}/recordAudio")
        return res['Enabled']

    def update_recordaudio(self, id: int, enabled: bool) -> None:
        """Turn recording of audio for the assignment

        :param id: Assignment Id
        :param enabled: `True` to turn audio recording on, `False` to turn it off
        """
        if not isinstance(enabled, bool):
            raise TypeError('enabled must be either True or False')

        self._make_call(method="patch",
                        path=f"{self.url}/{id}/recordAudio",
                        json={'Enabled': enabled})

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

        :returns: :class:`CalendarEvent` object
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

    def _get_assignment_by_id(self, **kwargs) -> AssignmentResult:
        # expecting fields, id, include_calendar_events
        try:
            return next(self._get_list(**kwargs))
        except StopIteration:
            raise ValueError("assignment was not found")
