from .base import HQBase
from .models import ExportJob
from .utils import parse_qidentity


class ExportApi(HQBase):
    _apiprefix: str = "/api/v2/export"

    def get_list(self, export_type=None, interview_status=None,
                 questionnaire_identity=None, export_status=None,
                 has_file=None):
        path = self.url
        params = {
            "exportType": export_type,
            "interviewStatus": interview_status,
            "questionnaireIdentity": parse_qidentity(questionnaire_identity),
            "exportStatus": export_status,
            "hasFile": has_file,
        }
        r = self._make_call('get', path, params=params)
        for item in r:
            yield ExportJob.from_dict(item)

    def get(self, questionnaire_identity: str,
            export_type: str = "Tabular", interview_status="All",
            export_path: str = ""):
        """Downloads latest available export file

        Parameters
        ----------
        questionnaire_identity : str
            Questionnaire id in format QuestionnaireGuid$Version

        export_type: str
            Format of the export data: ``Tabular``, ``STATA``, ``SPSS``, ``Binary``, ``DDI``, ``Paradata``

        interview_status: str
            What interviews to include in the export:
            ``All``, ``SupervisorAssigned``, ``InterviewerAssigned``, ``Completed``,
            ``RejectedBySupervisor``, ``ApprovedBySupervisor``, ``RejectedByHeadquarters``, ``ApprovedByHeadquarters``

        export_path: str
            Path to save the downloaded file
        """

        qid = parse_qidentity(questionnaire_identity)
        ret_list = self.get_list(
            export_type=export_type,
            questionnaire_identity=qid,
            interview_status=interview_status,
            export_status='Completed',
            has_file='true')
        try:
            download_link = next(ret_list).download_link
            return self._make_call('get', download_link, filepath=export_path, stream=True)
        except StopIteration:
            pass

    def get_info(self, job_id: int) -> ExportJob:
        path = self.url + '/{}'.format(job_id)
        return ExportJob.from_dict(self._make_call('get', path))

    def start(self, export_job: ExportJob) -> ExportJob:
        path = self.url
        return ExportJob.from_dict(self._make_call("post", path, json=export_job.to_json()))

    def cancel(self, job_id: int) -> None:
        response = self.get_info(job_id)
        if response.export_status == "Running":
            path = self.url + '{}'.format(job_id)
            _ = self._make_call('delete', path)
        else:
            print('No running export process was found')
