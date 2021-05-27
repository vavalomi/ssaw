import time
from datetime import datetime, timedelta, timezone

from .base import HQBase
from .models import ExportJob
from .utils import parse_qidentity


class ExportApi(HQBase):
    """ Set of functions to access and generate export files. """

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
            export_path: str = "",
            generate: bool = False, limit_age: int = None, limit_date: datetime = None, show_progress: bool = False):
        """Downloads latest available export file

        :param questionnaire_identity: Questionnaire id in format QuestionnaireGuid$Version

        :param export_type: Format of the export data:
            ``Tabular``, ``STATA``, ``SPSS``, ``Binary``, ``DDI``, ``Paradata``

        :param interview_status: What interviews to include in the export:
            ``All``, ``SupervisorAssigned``, ``InterviewerAssigned``, ``Completed``,
            ``RejectedBySupervisor``, ``ApprovedBySupervisor``, ``RejectedByHeadquarters``, ``ApprovedByHeadquarters``

        :param export_path: Path to save the downloaded file
        :param generate: generate new export if no existing result setisfies the specified filters
        :param limit_age: only return export file if created less than ``limit_age`` minutes ago
        :param limit_date: only return export file if created after the limit_date
        """

        qid = parse_qidentity(questionnaire_identity)
        common_args = {
            "questionnaire_identity": qid,
            "export_type": export_type,
            "interview_status": interview_status,
        }

        try:
            job = self._get_first_suitable(common_args, limit_age, limit_date)
            if job:
                return self._make_call('get', job.download_link, filepath=export_path, stream=True)
        except StopIteration:
            pass

        if not generate:
            return

        job = self.start(ExportJob(**common_args), wait=True, show_progress=show_progress)
        if job.has_export_file:
            response = self._make_call('get', job.download_link, filepath=export_path, stream=True)

        if show_progress:
            print(f"Archive was downloaded to {response}")

        return response

    def _get_first_suitable(self, common_args, limit_age=None, limit_date=None):
        ret_list = self.get_list(**common_args, export_status="Completed", has_file="true")

        if limit_date is None:
            limit_date = datetime(1970, 1, 1)

        if limit_date.tzinfo is None:
            limit_date = limit_date.astimezone()  # interpret date as in local timezone

        if limit_age:
            limit1 = datetime.now().astimezone() - timedelta(minutes=limit_age)
            if limit1 > limit_date:
                limit_date = limit1

        # start_date is returned in UTC, convert creation_limit as well
        limit_date = limit_date.astimezone(timezone(timedelta(0)))
        for job in ret_list:
            if job.start_date > limit_date:
                return job

    def get_info(self, job_id: int) -> ExportJob:
        path = self.url + '/{}'.format(job_id)
        return ExportJob.from_dict(self._make_call('get', path))

    def start(self, export_job: ExportJob, wait: bool = False, show_progress: bool = False) -> ExportJob:
        """Start new export job

        :param export_job: ``ExportJob`` object
        :param wait: if ``True`` will wait for the process to complete, otherwise, exit right away

        :returns: ``ExportJob`` object
        """
        path = self.url
        job = ExportJob.from_dict(self._make_call("post", path, json=export_job.to_json()))
        if wait:
            job = self.get_info(job.job_id)

            if show_progress:
                print("Generating...")

            while job.export_status != "Completed":
                time.sleep(1)
                if show_progress:
                    print(".", end="", flush=True)
                job = self.get_info(job.job_id)
            if show_progress:
                print()

        return job

    def cancel(self, job_id: int) -> None:
        response = self.get_info(job_id)
        if response.export_status == "Running":
            path = self.url + '{}'.format(job_id)
            _ = self._make_call('delete', path)
        else:
            print('No running export process was found')
