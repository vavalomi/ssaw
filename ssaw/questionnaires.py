from uuid import UUID

from .base import HQBase
from .models import Questionnaire, QuestionnaireListItem


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
            if 'TotalCount' in r:
                total_count = r['TotalCount']
                for item in r['Questionnaires']:
                    yield QuestionnaireListItem(**item)
            else:
                yield from ()
            page += 1

    def statuses(self):
        path = self.url + '/statuses'
        return self._make_call('get', path)

    def document(self, id: UUID, version: int) -> Questionnaire:
        path = self.url + '/{}/{}/document'.format(id, version)
        return self._make_call('get', path, parser=Questionnaire.parse_raw)

    def interviews(self, id: UUID, version: int):
        path = self.url + '/{}/{}/interviews'.format(id, version)
        return self._make_call('get', path)

    def update_recordaudio(self, id: UUID, version: int, enabled: bool):
        path = self.url + '/{}/{}/recordAudio'.format(id, version)
        return self._make_call('post', path, json={"Enabled": enabled})
