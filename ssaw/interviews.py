from html import escape
from typing import Generator

from sgqlc.operation import Operation

from .base import HQBase
from .headquarters_schema import (
    ComparableGuidOperationFilterInput,
    ComparableInt64OperationFilterInput,
    HeadquartersQuery,
    Interview,
    InterviewFilter,
    InterviewSort
)
from .models import InterviewAnswers
from .utils import fix_qid


class InterviewsApi(HQBase):
    """ Set of functions to access and manipulate Interviews. """

    _apiprefix = "/api/v1/interviews"

    @fix_qid(expects={'questionnaire_id': 'hex'})
    def get_list(self, fields: list = [], order: InterviewSort = None,
                 questionnaire_id=None, questionnaire_version=None,
                 skip: int = None, take: int = None, **kwargs
                 ) -> Generator[Interview, None, None]:

        interview_args = {
            "workspace": self.workspace
        }
        if order:
            interview_args["order"] = order
        if skip:
            interview_args["skip"] = skip
        if take:
            interview_args["take"] = take

        if questionnaire_id:
            kwargs["questionnaire_id"] = ComparableGuidOperationFilterInput(eq=questionnaire_id)
        if questionnaire_version:
            kwargs["questionnaire_version"] = ComparableInt64OperationFilterInput(eq=questionnaire_version)

        if kwargs:
            interview_args['where'] = InterviewFilter(**kwargs)

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

        op = Operation(HeadquartersQuery)
        q = op.interviews(**interview_args)
        q.nodes.__fields__(*fields)
        cont = self._make_graphql_call(op)

        res = (op + cont).interviews

        yield from res.nodes

    def get_info(self, interview_id: str) -> list:
        path = self.url + '/{}'.format(interview_id)
        ret = self._make_call('get', path)
        if "Answers" in ret:
            return InterviewAnswers.from_dict(ret["Answers"])

    def delete(self, interviewid, comment=''):
        return self._change_status(action='delete', interviewid=interviewid, comment=comment)

    def approve(self, interviewid, comment=''):
        return self._change_status(action='approve', interviewid=interviewid, comment=comment)

    def assign(self, interviewid, responsibleid, responsiblename=''):
        return self._reassign(action='assign', interviewid=interviewid,
                              responsibleid=responsibleid, responsiblename=responsiblename)

    def assign_supervisor(self, interviewid, responsibleid, responsiblename=''):
        return self._reassign(action='assignsupervisor', interviewid=interviewid,
                              responsibleid=responsibleid, responsiblename=responsiblename)

    @fix_qid(expects={'interview_id': 'string', 'question_id': 'hex'})
    def comment(self, interview_id, comment, question_id: str = None, variable: str = None, roster_vector: list = []):
        params = {'comment': escape(comment)}
        if roster_vector:
            params['rosterVector'] = roster_vector

        if variable:
            path = self.url + '/{}/comment-by-variable/{}'.format(interview_id, variable)
        else:
            if question_id:
                path = self.url + '/{}/comment/{}'.format(interview_id, question_id)
            else:
                raise TypeError("comment() either 'variable' or 'question_id' argument is required")

        self._make_call('post', path, params=params)

    @fix_qid(expects={'interview_id': 'string'})
    def history(self, interview_id):
        path = self.url + '/{}/history'.format(interview_id)
        return self._make_call('get', path)

    def hqapprove(self, interviewid, comment=''):
        return self._change_status(action='hqapprove', interviewid=interviewid, comment=comment)

    def hqreject(self, interviewid, comment=''):
        return self._change_status(action='hqreject', interviewid=interviewid, comment=comment)

    def hqunapprove(self, interviewid, comment=''):
        return self._change_status(action='hqunapprove', interviewid=interviewid, comment=comment)

    def reject(self, interviewid, comment=''):
        return self._change_status(action='reject', interviewid=interviewid, comment=comment)

    def stats(self, interviewid):
        pass

    def _change_status(self, interviewid, action, comment=''):
        path = self.url + '/{}/{}'.format(interviewid, action)
        return self._make_call('patch', path, params={'comment': escape(comment)})

    def _reassign(self, interviewid, action, responsibleid, responsiblename=''):
        path = self.url + '/{}/{}'.format(interviewid, action)
        payload = {
            'ResponsibleId': responsibleid,
            'ResponsibleName': responsiblename
        }
        _ = self._make_call('patch', path, json=payload)
        return True
