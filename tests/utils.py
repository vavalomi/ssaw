import os
import random
import re
import string

import requests

from ssaw import AssignmentsApi, UsersApi
from ssaw.exceptions import NotAcceptableError
from ssaw.models import Assignment


def create_user(client, user_name=None, password="Validpassword1", **kwargs):
    base_url = client.baseurl
    if not user_name:
        user_name = random_name()
    try:
        u = UsersApi(client).create(user_name=user_name, password=password, **kwargs)
    except NotAcceptableError:
        return
    payload = {
        "userId": u["UserId"],
        "password": password,
        "confirmPassword": password,
        "oldPassword": password
    }

    with requests.Session() as session:
        _ = session.post(f"{base_url}/Account/LogOn",
                         data={"UserName": user_name, "Password": password})
        _ = session.post(f"{base_url}/users/ChangePassword",
                         json=payload,
                         headers={"X-CSRF-TOKEN": session.cookies["CSRF-TOKEN"]})

    return u


def create_assignment(client, responsible, questionnaire_identity, identifying_data, **kwargs):
    newobj = Assignment(
        responsible=responsible,
        questionnaire_id=questionnaire_identity,
        quantity=5,
        identifying_data=identifying_data,
        **kwargs)

    return AssignmentsApi(client).create(newobj)


def import_questionnaire(base_url, questionnaire_id):
    url = f"{base_url}/api/QuestionnaireAutomation/ImportQuestionnaire"

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
        p = session.post(f"{base_url}/interviewerHq/StartNewInterview/{assignment_id}",
                         headers={"X-CSRF-TOKEN": session.cookies["CSRF-TOKEN"]})

    interview_id = p.json()['interviewId']
    if not interview_id:
        raise InterruptedError
    param = {"InterviewId": interview_id}
    data = {"answer": 2, "identity": "fe9719791f0bde796f28d74e66d67d12"}
    p = session.post(f"{base_url}/api/webinterview/commands/answerSingleOptionQuestion", params=param, json=data)

    return interview_id


def random_name(N=10):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=N))
