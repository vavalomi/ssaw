import time
from datetime import datetime, timedelta, timezone
from typing import Iterator, Optional, Union

from .base import HQBase
from .models import ExportJob, ExportJobResult, QuestionnaireIdentity
from .utils import parse_qidentity

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


class ExportApi(HQBase):
    """ Set of functions to access and generate export files. """

    EXPORT_STATUS = Literal['Created', 'Running', 'Completed', 'Fail', 'Canceled']
    EXPORT_TYPE = Literal['Tabular', 'STATA', 'SPSS', 'Binary', 'DDI', 'Paradata', 'AudioAudit']
    INTERVIEW_STATUS = Literal['All', 'SupervisorAssigned', 'InterviewerAssigned', 'Completed',
                               'RejectedBySupervisor', 'ApprovedBySupervisor', 'RejectedByHeadquarters',
                               'ApprovedByHeadquarters']

    _apiprefix: str = "/api/v2/export"

    def get_list(self,
                 questionnaire_identity: Optional[QuestionnaireIdentity] = None,
                 export_type: Optional[EXPORT_TYPE] = None,
                 interview_status: Optional[INTERVIEW_STATUS] = None,
                 export_status: Optional[EXPORT_STATUS] = None,
                 has_file: Optional[bool] = None) -> Iterator[ExportJobResult]:
        """
        Get list of all previosly executed export jobs

        :param questionnaire_identity: Questionnaire and version

        :param export_type: Format of the export data

        :param interview_status: What interviews to include in the export

        :param export_status: Status of the export job

        :param has_file: Whether the job has export file to download
        """

        path = self.url
        params = {
            "exportType": export_type,
            "interviewStatus": interview_status,
            "questionnaireIdentity": parse_qidentity(questionnaire_identity),
            "exportStatus": export_status,
            "hasFile": has_file,
        }
        r = self._make_call('get', path, params=params)
        if r:
            for item in r:
                yield ExportJobResult.model_validate(item)

    def get(self, questionnaire_identity: QuestionnaireIdentity,
            export_type: str = "Tabular", interview_status="All",
            export_path: str = "",
            generate: bool = False, limit_age: Optional[int] = None,
            limit_date: Optional[datetime] = None, show_progress: bool = False):
        """Downloads the latest available export file, optionally generating a new one.

        By default this method looks for an existing completed export on the server that
        matches the requested ``questionnaire_identity``, ``export_type`` and
        ``interview_status``.  If one is found it is downloaded immediately **without
        generating a new export**, even if that file was created days or weeks ago.

        .. note::
            Passing ``generate=True`` alone does **not** guarantee fresh data.  It only
            triggers a new export when *no* matching result exists at all on the server.
            To enforce freshness, combine it with ``limit_age`` or ``limit_date``::

                # Re-use an export only if it was created within the last 60 minutes;
                # otherwise generate a fresh one.
                ExportApi(client).get(
                    questionnaire_identity="...",
                    interview_status="All",
                    generate=True,
                    limit_age=60,
                )

        :param questionnaire_identity: Questionnaire id in format QuestionnaireGuid$Version

        :param export_type: Format of the export data:
            ``Tabular``, ``STATA``, ``SPSS``, ``Binary``, ``DDI``, ``Paradata``

        :param interview_status: What interviews to include in the export:
            ``All``, ``SupervisorAssigned``, ``InterviewerAssigned``, ``Completed``,
            ``RejectedBySupervisor``, ``ApprovedBySupervisor``, ``RejectedByHeadquarters``,
            ``ApprovedByHeadquarters``

        :param export_path: Directory path where the downloaded file will be saved

        :param generate: If ``True``, start a new export job when no suitable existing
            export is found.  Has no effect when a prior export already satisfies the
            filters (see note above).

        :param limit_age: Only accept an existing export if it was created less than
            ``limit_age`` minutes ago.  Older exports are ignored, triggering a new
            generation when ``generate=True``.

        :param limit_date: Only accept an existing export if it was created after this
            datetime.  Exports at or before this point are ignored.

        :param show_progress: Print progress messages to stdout while waiting for the
            export job to complete.
        """

        common_args = {
            "questionnaire_identity": parse_qidentity(questionnaire_identity),
            "export_type": export_type,
            "interview_status": interview_status,
        }

        try:
            job = self._get_first_suitable(common_args, limit_age, limit_date)
            if job:
                return self._make_call(method="get", path=job.links.download, filepath=export_path, stream=True)
        except StopIteration:
            print("No suitable export results were found")

        if not generate:
            return

        job = self.start(ExportJob(questionnaire_id=common_args["questionnaire_identity"],
                                   export_type=export_type,
                                   interview_status=interview_status),
                         wait=True, show_progress=show_progress)
        if job.has_export_file:
            response = self._make_call(method="get", path=job.links.download, filepath=export_path, stream=True)

            if show_progress:
                print(f"Archive was downloaded to {response}")

            return response

    def _get_first_suitable(self, common_args, limit_age=None, limit_date=None) -> Union[ExportJobResult, None]:
        ret_list = self.get_list(**common_args, export_status="Completed", has_file=True)

        # start_date is returned in UTC, convert creation_limit as well
        if limit_date is None:
            limit_date = datetime(2000, 1, 1, tzinfo=timezone.utc)
        elif limit_date.tzinfo:
            limit_date = limit_date.astimezone(timezone.utc)
        else:
            limit_date = limit_date.replace(tzinfo=timezone.utc)

        if limit_age:
            limit1 = datetime.now(timezone.utc) - timedelta(minutes=limit_age)
            if limit1 > limit_date:
                limit_date = limit1

        for job in ret_list:
            if job.start_date.replace(tzinfo=timezone.utc) > limit_date:
                return job

    def get_info(self, job_id: int) -> ExportJobResult:
        return ExportJobResult.model_validate(
            self._make_call(method="get", path=f"{self.url}/{job_id}"))

    def start(self, export_job: ExportJob, wait: bool = False, show_progress: bool = False,
              timeout: int = 300) -> ExportJobResult:
        """Start new export job

        :param export_job: ``ExportJobResult`` object
        :param wait: if ``True`` will wait for the process to complete, otherwise, exit right away
        :param timeout: maximum seconds to wait when ``wait=True`` (default 300)

        :returns: ``ExportJobResult`` object
        """
        path = self.url
        job = ExportJobResult.model_validate(
            self._make_call("post", path, json=export_job.model_dump(mode='json', by_alias=True, exclude_none=True))
        )
        if wait:
            job = self.get_info(job.job_id)

            if show_progress:
                print("Generating...")

            poll_interval = 5
            elapsed = 0
            while job.export_status not in ("Completed", "Fail", "Canceled") and elapsed < timeout:
                time.sleep(poll_interval)
                elapsed += poll_interval
                if show_progress:
                    print(".", end="", flush=True)
                job = self.get_info(job.job_id)
            if show_progress:
                print()

        return job

    def cancel(self, job_id: int) -> None:
        response = self.get_info(job_id)
        if response.export_status == "Running":
            _ = self._make_call(method="delete", path=f"{self.url}/{job_id}")
        else:
            print('No running export process was found')
