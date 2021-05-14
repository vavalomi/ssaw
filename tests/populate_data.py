import json
import os
from pathlib import Path

from dotenv import load_dotenv

import ssaw

from utils import (
    create_assignment,
    create_interview,
    create_user,
    import_questionnaire,
)

script_dir = os.path.abspath(os.path.dirname(__file__))

env_path = Path(os.path.join(script_dir, "env_vars.sh"))
load_dotenv(dotenv_path=env_path, verbose=True, override=True)
env_path = Path(os.path.join(script_dir, "env_vars_override.sh"))
if env_path.is_file():
    load_dotenv(dotenv_path=env_path, verbose=True, override=True)

base_url = os.environ.get("base_url")
designer_questionnaire_id = os.environ.get("designer_questionnaire_id")

# just to a list with more than one page
for _ in range(13):
    _ = import_questionnaire(base_url, designer_questionnaire_id)

client = ssaw.Client(base_url,
                     os.environ.get("SOLUTIONS_API_USER"),
                     os.environ.get("SOLUTIONS_API_PASSWORD"))
q = next(ssaw.QuestionnairesApi(client).get_list())

hq1 = create_user(client, user_name="hq1", password="Validpassword1", role="Headquarter")
super1 = create_user(client, user_name="super1", password="Validpassword1", role="Supervisor")
inter1 = create_user(client, user_name="inter1", password="Validpassword1", role="Interviewer", supervisor="super1")
inter2 = create_user(client, user_name="inter2", password="Validpassword1", role="Interviewer", supervisor="super1")

# just to a list with more than one page
for _ in range(13):
    create_user(client, password="Validpassword1", role="Supervisor")


identifying_data = [
    {"Variable": "address", "Answer": "123 Main Street"},
    {"Variable": "name", "Answer": "Jane Doe"}
]


for i in range(83):
    _ = create_assignment(client, "inter1", q.id, identifying_data)

for i in range(1003):
    interview_id = create_interview(base_url + '/primary', "inter1", "Validpassword1", 3)


admin_client = ssaw.Client(base_url,
                           os.environ.get("admin_username"),
                           os.environ.get("admin_password"))
ssaw.MapsApi(admin_client).upload(zip_file=os.path.join(os.path.dirname(os.path.realpath(__file__)), "maps.zip"))


# save parameters for test runs
version = 1
params = {
    'QuestionnaireId': '{}${}'.format(designer_questionnaire_id, version),
    'TemplateId': designer_questionnaire_id,
    'TemplateVersion': version,
    'InterviewId': interview_id,
    'Headquarters': hq1["UserId"],
    'SupervisorId': super1["UserId"],
    'InterviewerId': inter1["UserId"],
    'InterviewerId2': inter2["UserId"],
    'MapsArchive': 'tests/maps.zip',
    'MapFileName': 'map.tpk',
    'MapFileName2': 'map2.tpk',
    'MapUserName': 'inter1',
}

json.dump(params, open("params.json", mode="w"))

# generate export so that we have something in the list
job = ssaw.models.ExportJob(params['QuestionnaireId'])
r = ssaw.ExportApi(client).start(job)
