from uuid import UUID

from sgqlc.operation import Operation

from .base import HQBase
from .headquarters_schema import HeadquartersQuery
from .models import QuestionnaireDocument


class QuestionnairesApi(HQBase):
    """ Set of functions to access information on Questionnaires. """

    _apiprefix = "/api/v1/questionnaires"

    def get_list(self, fields: list = [], questionnaire_id: str = None, version: int = None,
                 skip: int = None, take: int = None):
        if not fields:
            fields = [
                "id",
                "questionnaire_id",
                "version",
                "title",
                "variable",
                "default_language_name",
            ]
        # we always have workspace parameter
        q_args = {
            "workspace": self.workspace
        }
        if questionnaire_id:
            q_args["questionnaire_id"] = questionnaire_id
        if version:
            q_args["version"] = version
        if skip:
            q_args["skip"] = skip
        if take:
            q_args["take"] = take

        op = Operation(HeadquartersQuery)
        q = op.questionnaires(**q_args)
        q.nodes.__fields__(*fields)

        cont = self._make_graphql_call(op)

        res = (op + cont).questionnaires

        yield from res.nodes

    def statuses(self):
        path = self.url + '/statuses'
        return self._make_call('get', path)

    def document(self, id: UUID, version: int) -> QuestionnaireDocument:
        path = self.url + '/{}/{}/document'.format(id, version)
        return self._make_call('get', path, parser=QuestionnaireDocument.parse_raw)

    def interviews(self, id: UUID, version: int):
        path = self.url + '/{}/{}/interviews'.format(id, version)
        return self._make_call('get', path)

    def update_recordaudio(self, id: UUID, version: int, enabled: bool):
        path = self.url + '/{}/{}/recordAudio'.format(id, version)
        return self._make_call('post', path, json={"Enabled": enabled})
