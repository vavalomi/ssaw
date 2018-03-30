from .utils import NotFoundError

class Interviews(object):
	def __init__(self, url, session):
		self.url = url + 'interviews'
		self.session = session

	def All(self):
		response = self.session.get(self.url)
		return response.json()

	def Details(self, interviewid):
		path = self.url + '/{}'.format(interviewid) + '/details'
		response = self.session.get(path)
		return response.json()

	def History(self, interviewid):
		path = self.url + '/{}'.format(interviewid) + '/history'
		response = self.session.get(path)
		return response.json()

	def Assign(self, interviewid, responsibleid, responsiblename=''):
		return self._reassign(action='assign', interviewid=interviewid, responsibleid=responsibleid, responsiblename=responsiblename)

	def Approve(self, interviewid, comment=''):
		return self._change_status(action='approve', interviewid=interviewid, comment=comment)

	def Reject(self, interviewid, comment=''):
		return self._change_status(action='reject', interviewid=interviewid, comment=comment)

	def HQApprove(self, interviewid, comment=''):
		return self._change_status(action='hqapprove', interviewid=interviewid, comment=comment)

	def HQReject(self, interviewid, comment=''):
		return self._change_status(action='hqreject', interviewid=interviewid, comment=comment)

	def HQUnapprove(self, interviewid, comment=''):
		return self._change_status(action='hqunapprove', interviewid=interviewid, comment=comment)

	def Delete(self, interviewid, comment=''):
		return self._change_status(action='delete', interviewid=interviewid, comment=comment)

	def AssignSupervisor(self, interviewid, responsibleid, responsiblename=''):
		return self._reassign(action='assignsupervisor', interviewid=interviewid, responsibleid=responsibleid, responsiblename=responsiblename)

	def _change_status(self, interviewid, action, comment=''):
		path = self.url + '/{}'.format(action)
		payload = {'Id': interviewid, 'Comment': comment}
		r = self.session.post(path, json = payload)
		if r.status_code == 404:
			raise NotFoundError('address not found')
		else:
			if r.status_code == 406:
				print(r.json()['Message'])
				return False
		return True

	def _reassign(self, interviewid, action, responsibleid, responsiblename=''):
		path = self.url + '/{}'.format(action)
		payload = {
			'Id': interviewid,
			'ResponsibleId': responsibleid,
			'ResponsibleName': responsiblename
		}
		r = self.session.post(path, json = payload)
		if r.status_code == 404:
			raise NotFoundError('address not found')
		else:
			if r.status_code == 406:
				print(r.json()['Message'])
				return False
		return True