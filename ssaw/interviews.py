from html import escape
from typing import Iterator, Optional, Union
from uuid import UUID

from .base import HQBase
from .headquarters_schema import (
    CalendarEvent,
    Interview,
    InterviewSort,
    InterviewsFilter,
)
from .models import InteriviewHistoryItem, InterviewAnswers
from .utils import filter_object, fix_qid, order_object


class InterviewsApi(HQBase):
    """ Set of functions to access and manipulate Interviews. """

    _apiprefix = "/api/v1/interviews"

    @fix_qid(expects={'questionnaire_id': 'hex'})
    def get_list(self, fields: Optional[list] = None, order=None,
                 skip: int = 0, take: Optional[int] = None,
                 where: Optional[InterviewsFilter] = None,
                 include_calendar_events: Union[list, tuple, bool] = False, **kwargs
                 ) -> Iterator[Interview]:
        """Get list of interviews

        :param fields: list of fields to return, of ommited, all fields wll be returned
        :param order: list of fields to sort the results by
        :param skip: number of interviews to skip
        :param take: number of interviews to return
        :param questionnaire_id: filter by specific questionnaire id
        :param questionnaire_variable: filter by questionnaire variable instead
        :param questionnaire_version: filter by specific version number
        :include_calendar_events: return calendar_event object as part of the fields

        :returns: list of :class:`Interview` objects
        """
        interview_args = {
            "workspace": self.workspace
        }
        if order:
            interview_args["order"] = order_object(InterviewSort, order)

        if where or kwargs:
            interview_args['where'] = filter_object(InterviewsFilter, where=where, **kwargs)

        if not fields:
            fields = [
                'id',
                'questionnaire_id',
                'questionnaire_version',
                'assignment_id',
                'responsible_id',
                'errors_count',
                'status',
            ]

        op = self._graphql_query_operation('interviews', interview_args)
        q = op.interviews
        q.nodes.__fields__(*fields)
        if include_calendar_events:
            if type(include_calendar_events) in [list, tuple]:
                q.nodes.calendar_event.__fields__(*include_calendar_events)
            else:
                q.nodes.calendar_event.__fields__()

        yield from self._get_full_list(op, 'interviews', skip=skip, take=take)

    def get_info(self, interview_id: UUID) -> InterviewAnswers:
        path = f"{self.url}/{interview_id}"
        ret = self._make_call('get', path)
        if "Answers" in ret:
            obj = InterviewAnswers()
            obj.from_dict(ret["Answers"])
            return obj

    def delete(self, interviewid: UUID, comment: str = None):
        return self._change_status(action='delete', interviewid=interviewid, comment=comment)

    def get_calendar_event(self, interview_key: str) -> CalendarEvent:
        """Get calendar event associated with the interview
        """
        interview = self._get_interview_by_key(fields=["id"],
                                               key=interview_key,
                                               include_calendar_events=True)

        return interview.calendar_event

    def set_calendar_event(self, interview_key: str, new_start: str,
                           start_timezone: str, comment: Optional[str] = None) -> CalendarEvent:
        """Add new calendar event to the interview, or update the existing one

        :param interview_key: key of the interview to update
        :param new_start: start date of the calendar event
        :param start_timezone: timezone string for the start date
        :param comment: add comment to the calendar event

        :returns: :class:`CalendarEvent` object
        """
        interview = self._get_interview_by_key(fields=["id"],
                                               key=interview_key,
                                               include_calendar_events=["public_key"])

        kwargs = {
            "new_start": new_start,
            "start_timezone": start_timezone,
            "comment": comment
        }
        if hasattr(interview.calendar_event, "public_key"):
            kwargs["method_name"] = "update_calendar_event"
            kwargs["public_key"] = interview.calendar_event.public_key
        else:
            kwargs["method_name"] = "add_interview_calendar_event"
            kwargs["interview_id"] = interview.id

        return self._call_mutation(**kwargs)

    def delete_calendar_event(self, interview_key: str) -> CalendarEvent:
        """Remove calendar event associated with the interview
        """
        interview = self._get_interview_by_key(fields=["id"],
                                               key=interview_key,
                                               include_calendar_events=["public_key"])

        if hasattr(interview.calendar_event, "public_key"):
            return self._call_mutation(method_name="delete_calendar_event",
                                       public_key=interview.calendar_event.public_key)

    def approve(self, interviewid, comment=''):
        return self._change_status(action='approve', interviewid=interviewid, comment=comment)

    def assign(self, interviewid, responsibleid, responsiblename=''):
        return self._reassign(action='assign', interviewid=interviewid,
                              responsibleid=responsibleid, responsiblename=responsiblename)

    def assign_supervisor(self, interviewid, responsibleid, responsiblename=''):
        return self._reassign(action='assignsupervisor', interviewid=interviewid,
                              responsibleid=responsibleid, responsiblename=responsiblename)

    @fix_qid(expects={'interview_id': 'string', 'question_id': 'hex'})
    def comment(self, interview_id, comment, question_id: str = None, variable: str = None, roster_vector: list = None):
        params = {'comment': escape(comment)}
        if roster_vector:
            params['rosterVector'] = roster_vector

        if variable:
            path = f"{self.url}/{interview_id}/comment-by-variable/{variable}"
        elif question_id:
            path = f"{self.url}/{interview_id}/comment/{question_id}"
        else:
            raise TypeError("comment() either 'variable' or 'question_id' argument is required")

        self._make_call('post', path, params=params)

    @fix_qid(expects={'interview_id': 'string'})
    def history(self, interview_id):
        path = f"{self.url}/{interview_id}/history"
        ret = self._make_call('get', path)
        for item in ret["Records"]:
            yield InteriviewHistoryItem.parse_obj(item)

    def hqapprove(self, interviewid, comment=''):
        return self._change_status(action='hqapprove', interviewid=interviewid, comment=comment)

    def hqreject(self, interviewid, comment=''):
        return self._change_status(action='hqreject', interviewid=interviewid, comment=comment)

    def hqunapprove(self, interviewid, comment=''):
        return self._change_status(action='hqunapprove', interviewid=interviewid, comment=comment)

    def reject(self, interviewid, comment=''):
        return self._change_status(action='reject', interviewid=interviewid, comment=comment)

    def _change_status(self, interviewid, action, comment=None):
        path = f"{self.url}/{interviewid}/{action}"
        params = {'comment': escape(comment)} if comment else {}
        return self._make_call('patch', path, params=params)

    def _reassign(self, interviewid, action, responsibleid, responsiblename=''):
        path = f"{self.url}/{interviewid}/{action}"
        payload = {
            'ResponsibleId': responsibleid,
            'ResponsibleName': responsiblename
        }
        _ = self._make_call('patch', path, json=payload)
        return True

    def _get_interview_by_key(self, **kwargs):
        # expecting fields, key, include_calendar_events
        try:
            interview = next(self.get_list(**kwargs))
        except StopIteration:
            raise ValueError("interview was not found")

        return interview
