class Assignment(object):
    def __init__(self, responsible, quantity, questionnaire_id,
        email='', password='', webmode=False,
        audio_recording_enabled=False, comments=''):

        self.responsible = responsible
        self.quantity = quantity
        self.questionnaire_id = questionnaire_id
        self.email = email
        self.password = password
        self.webmode = webmode
        self.audio_recording_enabled = audio_recording_enabled
        self.identifying_data = []
        self.comments = comments

    @classmethod
    def from_dict(cls, dict):
        obj = cls(
            responsible = dict['ResponsibleName'],
            quantity = dict['Quantity'], 
            questionnaire_id = dict['QuestionnaireId'],
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

class Questionnaire(object):
    def __init__(self, dict):
        self.questionnaire_identity = dict['QuestionnaireIdentity']
        self.questionnaire_id = dict['QuestionnaireId']
        self.version = dict['Version']
        self.title = dict['Title']
        self.variable = dict['Variable']
        self.last_entry_date = dict['LastEntryDate']

    @classmethod
    def from_dict(cls, dict):
        return cls(dict) 