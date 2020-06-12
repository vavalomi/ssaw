from .base import HQBase
from .exceptions import NotFoundError, GraphQLError
from .headquarters_schema import headquarters_schema, InterviewFilter, Interview
from sgqlc.operation import Operation
from typing import Generator

class InterviewsApi(HQBase):
    _apiprefix = "/api/v1/interviews"

    def get_list(self, fields: list= (), **kwargs) -> Generator[Interview, None, None]:
        where = InterviewFilter(**kwargs)
        take = 20
        skip = 0
        filtered_count = 21
        if not fields:
            fields = (
                'id',
                'questionnaire_id',
                'questionnaire_version',
                'assignment_id',
                'responsible_id',
                'errors_count',
                'status',
            )
        while skip < filtered_count:  
            op = Operation(headquarters_schema.HeadquartersQuery)  
            q = op.interviews(take=take, skip=skip, where=where)
            q.__fields__('filtered_count')
            q.nodes.__fields__(*fields)
            print(op)
            cont = self.endpoint(op)
            errors = cont.get('errors')
            if errors:
                raise GraphQLError(errors[0]['message'])
            res = (op + cont).interviews

            filtered_count = res.filtered_count
            yield from res.nodes
            skip += take

    def get_info(self, interviewid):
        path = self.url + '/{}'.format(interviewid)
        return self._make_call('get', path)

    def delete(self, interviewid, comment=''):
        return self._change_status(action='delete', interviewid=interviewid, comment=comment)

    def answers(self, interviewid):
        pass

    def approve(self, interviewid, comment=''):
        return self._change_status(action='approve', interviewid=interviewid, comment=comment)

    def assign(self, interviewid, responsibleid, responsiblename=''):
        return self._reassign(action='assign', interviewid=interviewid, responsibleid=responsibleid, responsiblename=responsiblename)

    def assign_supervisor(self, interviewid, responsibleid, responsiblename=''):
        return self._reassign(action='assignsupervisor', interviewid=interviewid, responsibleid=responsibleid, responsiblename=responsiblename)

    def comment(self, interviewid, comment, questionid=None, variable=''):
        pass

    def history(self, interviewid):
        path = self.url + '/{}'.format(interviewid) + '/history'
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
        path = self.url + '/{}/{}?comment={}'.format(interviewid, action, comment)
        return self._make_call('patch', path)

    def _reassign(self, interviewid, action, responsibleid, responsiblename=''):
        path = self.url + '/{}/{}'.format(interviewid, action)
        payload = {
            'ResponsibleId': responsibleid,
            'ResponsibleName': responsiblename
        }
        r = self._make_call('patch', path, json = payload)
        return True