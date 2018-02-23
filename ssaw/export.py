import re
import os
from .utils import NotFoundError

class Export(object):
	def __init__(self, url, session):
		self.url = url + 'export'
		self.session = session

	def Get(self, id, exportpath, exporttype='Tabular', generate=False):
		response = self.GetInfo(id, exporttype)
		if response['HasExportedFile'] == True:
			path = self.url + '/{}/{}'.format(exporttype, id)
			response = self.session.get(path, stream=True)

			d = response.headers['content-disposition']
			fname = re.findall("filename\*=utf-8''(.+)", d)[0]
			print(fname)
			outfile = os.path.join(exportpath, fname)
			with open(outfile, 'wb') as f:
				for chunk in response.iter_content(chunk_size=1024): 
					if chunk: # filter out keep-alive new chunks
						f.write(chunk)
		return outfile


	def GetInfo(self, id, exporttype='Tabular'):
		path = self.url + '/{}/{}'.format(exporttype, id) + '/details'
		response = self.session.get(path)
		if response.status_code == 200:
			return response.json()
		else:
			print(response.status_code)
			raise NotFoundError('QuestionnaireId')

	def Start(self, id, exporttype='Tabular'):
		status = 0
		response = self.GetInfo(id, exporttype)
		if response['ExportStatus'] == 'NotStarted':
			path = self.url + '/{}/{}'.format(exporttype, id) + '/start'
			response = self.session.post(path)
			status = response.status_code
		else:
			print('Export is currently running')

		return status

	def Cancel(self, id, exporttype='Tabular'):
		status = 0
		response = self.GetInfo(id, exporttype)
		if response['ExportStatus'] != 'NotStarted':
			path = self.url + '/{}/{}'.format(exporttype, id) + '/cancel'
			response = self.session.post(path)
			status = response.status_code
		else:
			print('No running export process was found')

		return status
