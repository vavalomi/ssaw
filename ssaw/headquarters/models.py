class Assignment(object):
    def __init__(self, dict):
        self.id = dict['Id']
        self.responsible_id = dict['ResponsibleId']
        self.responsible_name = dict['ResponsibleName']
        self.questionnaire_id = dict['QuestionnaireId']
        self.interviews_count = dict['InterviewsCount']
        self.quantity = dict['Quantity']
        self.archived = dict['Archived']
        self.created_utc = dict['CreatedAtUtc']
        self.updated_utc = dict['UpdatedAtUtc']
        self.email = dict['Email']
        self.password = dict['Password']
        self.webmode = dict['WebMode']

class Questionnaire(object):
    def __init__(self, dict):
        self.questionnaire_identity = dict['QuestionnaireIdentity']
        self.questionnaire_id = dict['QuestionnaireId']
        self.version = dict['Version']
        self.title = dict['Title']
        self.variable = dict['Variable']
        self.last_entry_date = dict['LastEntryDate']