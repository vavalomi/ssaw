from .base import HQBase
from .exceptions import IncompleteQuestionnaireIdError
from .models import QuestionnaireListItem
from .designer import import_questionnaire_json

class QuestionnairesApi(HQBase):
    _apiprefix = "/api/v1/questionnaires"

    def get_list(self):
        path = self.url
        page_size = 10
        page = 1
        total_count = 11
        params = {
            'offset': page,
            'limit': page_size
        }
        while page * page_size < total_count:
            params['page'] = page
            r = self._make_call('get', path, params=params)
            total_count = r['TotalCount']
            for item in r['Questionnaires']:
                yield QuestionnaireListItem.from_dict(item)
            page += 1

    def statuses(self):
        path = self.url + '/statuses'
        return self._make_call('get', path)

    def document(self, id, version):
        path = self.url + '/{}/{}/document'.format(id, version)
        return self._make_call('get', path, parser=import_questionnaire_json)

    def interviews(self, id, version):
        path = self.url + '/{}/{}/interviews'.format(id, version)
        return self._make_call('get', path)

    def update_recordaudio(self, id, version):
        """POST /api/v1/questionnaires/{id}/{version}/recordAudio"""
        pass