from .utils import to_hex, to_qidentity


class Assignment(object):
    def __init__(self, responsible, quantity, questionnaire_id,
                 identifying_data=None, email='', password='', webmode=False,
                 audio_recording_enabled=False, comments=''):
        """[summary]

        Parameters
        ----------
        responsible : [type]
            [description]
        quantity : [type]
            [description]
        questionnaire_id : [type]
            [description]
        email : str, optional
            [description], by default ''
        password : str, optional
            [description], by default ''
        webmode : bool, optional
            [description], by default False
        audio_recording_enabled : bool, optional
            [description], by default False
        comments : str, optional
            [description], by default ''
        """

        self.responsible = responsible
        self.quantity = quantity
        self.questionnaire_id = questionnaire_id
        self.identifying_data = identifying_data
        self.email = email
        self.password = password
        self.webmode = webmode
        self.audio_recording_enabled = audio_recording_enabled
        self.comments = comments

    def __str__(self):
        return(str(self.__dict__))

    @classmethod
    def from_dict(cls, dict):
        obj = cls(
            responsible=dict['ResponsibleName'],
            quantity=dict['Quantity'],
            questionnaire_id=dict['QuestionnaireId'],
            identifying_data=dict['IdentifyingData'] if 'IdentifyingData' in dict else [
            ],
            email=dict['Email'],
            password=dict['Password'],
            webmode=dict['WebMode']
        )
        setattr(obj, 'id', dict['Id'])
        setattr(obj, 'responsible_id', dict['ResponsibleId'])
        setattr(obj, 'interviews_count', dict['InterviewsCount'])
        setattr(obj, 'archived', dict['Archived'])
        setattr(obj, 'created_utc', dict['CreatedAtUtc'])
        setattr(obj, 'updated_utc', dict['UpdatedAtUtc'])
        if 'IsAudioRecordingEnabled' in dict:
            setattr(obj, 'audio_recording_enabled',
                    dict['IsAudioRecordingEnabled'])
        return obj

    def to_json(self):
        return {
            "Responsible": self.responsible,
            "Quantity": self.quantity,
            "QuestionnaireId": self.questionnaire_id,
            "Email": self.email,
            "Password": self.password,
            "WebMode": self.webmode,
            "IsAudioRecordingEnabled": self.audio_recording_enabled,
            "Comments": self.comments
        }


class QuestionnaireListItem(object):
    def __init__(self, dict):
        self.questionnaire_identity = dict['QuestionnaireIdentity']
        self.questionnaire_id = dict['QuestionnaireId']
        self.version = dict['Version']
        self.title = dict['Title']
        self.variable = dict['Variable']
        self.last_entry_date = dict['LastEntryDate']

    def __str__(self):
        return(str(self.__dict__))

    @classmethod
    def from_dict(cls, dict):
        return cls(dict)


class ExportJob(object):
    def __init__(self,
                 questionnaire_identity,
                 export_type='Tabular',
                 interview_status='All',
                 from_date=None,
                 to_date=None,
                 access_token=None,
                 storage_type=None):
        """[summary]

        Parameters
        ----------
        questionnaire_identity : [type]
            [description]
        export_type : str, optional
            [description], by default 'Tabular'
        interview_status : str, optional
            [description], by default 'All'
        from_date : [type], optional
            [description], by default None
        to_date : [type], optional
            [description], by default None
        access_token : [type], optional
            [description], by default None
        storage_type : [type], optional
            [description], by default None
        """

        if type(questionnaire_identity) is tuple:
            (questionnaire_id, questionnaire_version) = questionnaire_identity
            questionnaire_identity = to_qidentity(
                questionnaire_id, questionnaire_version)

        self.questionnaire_identity = questionnaire_identity
        self.export_type = export_type
        self.interview_status = interview_status
        self.from_date = from_date
        self.to_date = to_date
        self.access_token = access_token
        self.storage_type = storage_type
        self._export_status: str
        self._has_export_file: bool
        self._cancel_link: str
        self._download_link: str

    @property
    def export_status(self) -> str:
        return self._export_status

    @property
    def has_export_file(self) -> bool:
        return self._has_export_file

    @property
    def cancel_link(self) -> str:
        return self._cancel_link

    @property
    def download_link(self) -> str:
        return self._download_link

    def __str__(self) -> str:
        return(str(self.__dict__))

    @classmethod
    def from_dict(cls, dict):
        obj = cls(
            export_type=dict['ExportType'],
            questionnaire_identity=dict['QuestionnaireId'],
            interview_status=dict['InterviewStatus'],
            from_date=dict['From'] if 'From' in dict else None,
            to_date=dict['To'] if 'To' in dict else None,
            access_token=dict['AccessToken'] if 'AccessToken' in dict else None,
            storage_type=dict['StorageType'] if 'StorageType' in dict else None
        )
        setattr(obj, 'job_id', dict['JobId'])
        setattr(obj, '_export_status', dict['ExportStatus'])
        setattr(obj, 'start_date', dict['StartDate'])
        setattr(obj, 'complete_date', dict['CompleteDate'])
        setattr(obj, 'progress', dict['Progress'])
        if 'ETA' in dict:
            setattr(obj, 'eta', dict['ETA'])
        if 'Links' in dict:
            if 'Cancel' in dict['Links']:
                setattr(obj, '_cancel_link', dict['Links']['Cancel'])
            if 'Download' in dict['Links']:
                setattr(obj, '_download_link', dict['Links']['Download'])
        setattr(obj, '_has_export_file', dict['HasExportFile'])
        return obj

    def to_json(self):
        ret = {
            "ExportType": self.export_type,
            "QuestionnaireId": self.questionnaire_identity,
            "InterviewStatus": self.interview_status,
            "From": self.from_date,
            "To": self.to_date,
            "AccessToken": self.access_token,
            "StorageType": self.storage_type,
        }
        return {k: v for k, v in ret.items() if v is not None}


class InterviewAnswers(object):
    def __init__(self, answers: dict):
        data = {}
        variables = {}
        self._raw_data = answers["Answers"]
        for ans in self._raw_data:
            val = ans["Answer"]
            id = to_hex(ans["QuestionId"]["Id"])
            variables[ans["VariableName"]] = id
            if val is None:
                continue
            if len(ans["QuestionId"]["RosterVector"]) > 0:
                key = "_".join([id, ] + [str(r)
                                         for r in ans["QuestionId"]["RosterVector"]])
            else:
                key = id
            data[key] = val
        self._data = data
        self._variables = variables

    def __str__(self) -> str:
        return(str(self._raw_data))

    def get_answer(self, variable: str = None, question_id: str = None, roster_vector: list = []):
        if variable:
            if variable in self._variables:
                key = self._variables[variable]
            else:
                raise TypeError("get_answer() variable not found")
        else:
            if question_id:
                key = to_hex(question_id)
            else:
                raise TypeError(
                    "get_anwer() either 'variable' or 'question_id' argument is required")

        if roster_vector:
            key = "_".join([key, ] + [str(r) for r in roster_vector])

        if key in self._data:
            return self._data[key]
        else:
            return None

    def __iter__(self):
        return iter(self._raw_data)
