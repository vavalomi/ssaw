from .base import HQBase
from .exceptions import NotFoundError

class Interviews(HQBase):

    @property
    def url(self):
        return self._baseurl + '/interviews'

    def __call__(self):
        """GET /api/v1/interviews
        """

        path = self.url
        return self._make_call('get', path)

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
        path = self.url + '/{}'.format(action)
        payload = {
            'Id': interviewid,
            'ResponsibleId': responsibleid,
            'ResponsibleName': responsiblename
        }
        r = self._make_call('post', path, json = payload)
        r = self.session.post(path, json = payload)
        return True