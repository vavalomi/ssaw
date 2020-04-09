from .utils import to_qidentity

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
        print(dict)
        obj = cls(
            responsible = dict['ResponsibleName'],
            quantity = dict['Quantity'], 
            questionnaire_id = dict['QuestionnaireId'],
            identifying_data=dict['IdentifyingData'] if 'IdentifyingData' in dict else [],
            email = dict['Email'],
            password = dict['Password'],
            webmode = dict['WebMode']
        )
        setattr(obj, 'id', dict['Id'])
        setattr(obj, 'responsible_id', dict['ResponsibleId'])
        setattr(obj, 'interviews_count', dict['InterviewsCount'])
        setattr(obj, 'archived', dict['Archived'])
        setattr(obj, 'created_utc', dict['CreatedAtUtc'])
        setattr(obj, 'updated_utc', dict['UpdatedAtUtc'])
        if 'IsAudioRecordingEnabled' in dict:
            setattr(obj, 'audio_recording_enabled', dict['IsAudioRecordingEnabled'])
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

class InterviewListItem(object):
    def __init__(self, dict):
        self.interview_id = dict['InterviewId']
        self.questionnaire_id = dict['QuestionnaireId']
        self.questionnaire_version = dict['QuestionnaireVersion']
        self.assignment_id = dict['AssignmentId']
        self.responsible = dict['ResponsibleName']
        self.error_count = dict['ErrorsCount']
        self.status = dict['Status']
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
            questionnaire_identity = to_qidentity(questionnaire_id, questionnaire_version)

        self.questionnaire_identity = questionnaire_identity
        self.export_type = export_type
        self.interview_status = interview_status
        self.from_date = from_date
        self.to_date = to_date
        self.access_token = access_token
        self.storage_type = storage_type

    def __str__(self):
        return(str(self.__dict__))

    @classmethod
    def from_dict(cls, dict):
        obj = cls(
            export_type = dict['exportType'],
            questionnaire_identity = dict['questionnaireId'],
            interview_status = dict['interviewStatus'],
            from_date = dict['from'] if 'from' in dict else None,
            to_date = dict['to'] if 'to' in dict else None,
            access_token = dict['accessToken'] if 'accessToken' in dict else None,
            storage_type = dict['storageType'] if 'storageType' in dict else None
        )
        setattr(obj, 'job_id', dict['jobId'])
        setattr(obj, 'export_status', dict['exportStatus'])
        setattr(obj, 'start_date', dict['startDate'])
        setattr(obj, 'complete_date', dict['completeDate'])
        setattr(obj, 'progress', dict['progress'])
        if 'eta' in dict:
            setattr(obj, 'eta', dict['eeta'])
        if 'links' in dict:
            if 'cancel' in dict['links']:
                setattr(obj, 'cancel_link', dict['links']['cancel'])
            if 'download' in dict['links']:
                setattr(obj, 'download_link', dict['links']['download'])
        setattr(obj, 'has_export_file', dict['hasExportFile'])
        return obj

    def to_json(self):
        ret = {
                "exportType": self.export_type,
                "questionnaireId": self.questionnaire_identity,
                "interviewStatus": self.interview_status,
                "from": self.from_date,
                "to": self.to_date,
                "accessToken": self.access_token,
                "storageType": self.storage_type,
            }
        return {k: v for k, v in ret.items() if v is not None}