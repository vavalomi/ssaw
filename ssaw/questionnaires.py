import csv
import zipfile
from io import TextIOWrapper
from tempfile import TemporaryDirectory
from uuid import UUID

from sgqlc.operation import Operation

from .base import HQBase
from .headquarters_schema import HeadquartersQuery
from .interviews import InterviewsApi
from .models import AssignmentWebLink, QuestionnaireDocument


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
            ]
        # we always have workspace parameter
        q_args = {
            "workspace": self.workspace
        }
        if questionnaire_id:
            q_args["id"] = questionnaire_id
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
        api = InterviewsApi(client=self._hq)
        return api.get_list(questionnaire_id=id, questionnaire_version=version)

    def update_recordaudio(self, id: UUID, version: int, enabled: bool):
        path = self.url + '/{}/{}/recordAudio'.format(id, version)
        return self._make_call('post', path, json={"Enabled": enabled})

    def download_web_links(self, id: UUID, version: int, path: str = None):
        """Download links for the assignments in Web Mode.

        :param id: questionnaire id
        :param version: questionnaire version
        :param path: optionally specify the download location

        if `path` is specified, zip archive will be downloaded to the location.
        Otherwise, list of ``AssignmentWebLink`` objects will be returned
        """
        common_args = {
            "method": "get",
            "path": f"{self._hq.baseurl}/{self.workspace}/api/LinksExport/Download/{id}${version}",
            "stream": True,
            "use_login_session": True,
        }
        if path:
            return self._make_call(**common_args, filepath=path)

        with TemporaryDirectory() as tempdir:
            outfile = self._make_call(**common_args, filepath=tempdir)
            with zipfile.ZipFile(outfile, "r") as zip_ref:
                with zip_ref.open("interviews.tab") as infile:
                    data = csv.DictReader(TextIOWrapper(infile, 'utf-8'), delimiter="\t")
                    return [AssignmentWebLink(**row) for row in data]
