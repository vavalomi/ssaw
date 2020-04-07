from .base import HQBase
from .exceptions import NotFoundError
from .models import InterviewListItem

class Interviews(HQBase):
    _apiprefix = "/api/v1/interviews"

    def get_list(self, questionnaire_id = None, questionnaire_version = None):
        path = self.url
        page_size = 10
        page = 1
        total_count = 11
        params = {
            'page': page,
            'pageSize': page_size,
            'questionnaireId': questionnaire_id,
            'questionnaireVersion': questionnaire_version
        }
        while page * page_size < total_count:
            params['page'] = page
            r = self._make_call('get', path, params=params)
            total_count = r['TotalCount']
            for item in r['Interviews']:
                yield InterviewListItem.from_dict(item)
            page += 1

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