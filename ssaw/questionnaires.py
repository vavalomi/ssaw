import csv
import zipfile
from io import TextIOWrapper
from tempfile import TemporaryDirectory
from typing import List, Optional
from uuid import UUID

from .base import HQBase
from .interviews import InterviewsApi
from .models import AssignmentWebLink, QuestionnaireDocument


class QuestionnairesApi(HQBase):
    """ Set of functions to access information on Questionnaires. """

    _apiprefix = "/api/v1/questionnaires"

    def get_list(self, fields: Optional[List[str]] = None, questionnaire_id: Optional[str] = None,
                 version: Optional[int] = None, skip: int = 0, take: Optional[int] = None):
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

        op = self._graphql_query_operation('questionnaires', q_args)
        op.questionnaires.nodes.__fields__(*fields)

        yield from self._get_full_list(op, 'questionnaires', skip=skip, take=take)

    def statuses(self):
        return self._make_call(method="get", path=f"{self.url}/statuses")

    def document(self, id: UUID, version: int) -> QuestionnaireDocument:
        return QuestionnaireDocument.parse_obj(
            self._make_call(method="get", path=f"{self.url}/{id}/{version}/document"))

    def interviews(self, id: UUID, version: int):
        api = InterviewsApi(client=self._hq)
        return api.get_list(questionnaire_id=id, questionnaire_version=version)

    def update_recordaudio(self, id: UUID, version: int, enabled: bool):
        _ = self._make_call(method="post",
                            path=f"{self.url}/{id}/{version}/recordAudio",
                            json={"Enabled": enabled})

    def download_web_links(self, id: UUID, version: int, path: Optional[str] = None):
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
                    return [AssignmentWebLink.parse_obj(row) for row in data]
