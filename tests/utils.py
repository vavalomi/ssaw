import os
import random
import requests
import re
import string

from ssaw import AssignmentsApi
from ssaw.models import Assignment

def create_assignment(client, responsible, questionnaire_identity, identifying_data):
    newobj = Assignment(
        responsible=responsible,
        questionnaire_id=questionnaire_identity,
        quantity=5,
        identifying_data=identifying_data)

    return AssignmentsApi(client).create(newobj)

def import_questionnaire(base_url, questionnaire_id):
    url = base_url + "/api/QuestionnaireAutomation/ImportQuestionnaire"

    data = {
        "QuestionnaireId": questionnaire_id,
        "DesignerUsername": os.environ.get("designer_username"),
        "DesignerPassword": os.environ.get("designer_password"),
        "ShouldUpgradeAssignments": False,
        "MigrateFrom": None,
        "MigrateFromVersion": None,
        "Comment": "Auto-imported for testing"
    }
    auth = (os.environ.get("admin_username"), os.environ.get("admin_password"))
    return requests.post(url, json=data, auth=auth)

def get_interview_id(text):
    m = re.search("/WebInterview/(.+?)/Cover", text)
    if m:
        return m.group(1)

def create_interview(base_url, user_name, password, assignment_id):
    login_url = base_url + "/Account/LogOn"

    with requests.Session() as session:
        _ = session.post(login_url, data={"UserName": user_name, "Password": password})
        p = session.post(base_url + "/interviewerHq/StartNewInterview/{}".format(assignment_id))

    interview_id = get_interview_id(p.text)
    if not interview_id:
        raise InterruptedError
    param = {"InterviewId": interview_id}
    data = {"answer": 2, "identity":"fe9719791f0bde796f28d74e66d67d12"}
    p = session.post(base_url + "/api/webinterview/commands/answerSingleOptionQuestion", params=param, json=data)

    return interview_id

def upload_maps(base_url, zip_file):
    login_url = base_url + "/Account/LogOn"

    user_name = os.environ.get("admin_username")
    password = os.environ.get("admin_password")
    with requests.Session() as session:
        _ = session.post(login_url, data={"UserName": user_name, "Password": password})
        _ = session.post(base_url + "/api/MapsApi/Upload", files={'file': open(zip_file, 'rb')})

def random_name(N=10):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=N))
