# SSAW: Python wrapper for the Survey Solutions HTTP API

[![Python package](https://github.com/vavalomi/ssaw/workflows/Python%20package/badge.svg)](https://github.com/vavalomi/ssaw/actions)
[![codecov](https://codecov.io/gh/vavalomi/ssaw/branch/master/graph/badge.svg)](https://codecov.io/gh/vavalomi/ssaw)
[![PyPI version](https://badge.fury.io/py/ssaw.svg)](https://badge.fury.io/py/ssaw)
[![Documentation Status](https://readthedocs.org/projects/ssaw/badge/?version=latest)](https://ssaw.readthedocs.io/en/latest/?badge=latest)

Read more about Survey Solutions at <https://mysurvey.solutions>

Details on API at <https://demo.mysurvey.solutions/apidocs/index>

## Quickstart

Install SSAW:

```shell
pip install ssaw
```

Initialize connection with the server:

```python
import ssaw

client = ssaw.Client('https://demo.mysurvey.solutions', 'api_user', 'api_password')
```

Get list of questionnaires:

```python
for q in ssaw.QuestionnairesApi(client).get_list():
    print(q.title)
```

Download latest export file in SPSS format:

```python
from ssaw import ExportApi

# without export_path parameter file will be saved in the current working directory
filename = ExportApi(client).get(export_type="SPSS", questionnaire_identity="64136490cbc24a71a1df10f4b7115599$1")
```

Create new assignment:

```python
from ssaw.models import Assignment
from ssaw import AssignmentsApi, QuestionnairesApi
from ssaw.models import InterviewAnswers

identifying_data = [
    {"Variable": "address", "Answer": "123 Main Street"},
    {"Variable": "name", "Answer": "Jane Doe"}
]
newobj = Assignment(
    responsible="inter1",
    questionnaire_id="",
    quantity=5,
    identifying_data=identifying_data)

res = AssignmentsApi(client).create(newobj)
print(res.id)

# More advanced example with data-preloading
q_doc = QuestionnairesApi(client).document(id="00000000-0000-0000-0000-000000000000", version=1)

d = InterviewAnswers(q_doc)
d.set_answer(variable="address", answer="123 Main Street")
d.set_answer(variable="name", answer="Jane Doe")
d.set_answer(variable="member_name", answer="Jane", roster_vector=0)  # question in the first-level roster
d.set_answer(variable="pet", answer="Cat", roster_vector=[0, 0])  # second-level roster

newobj = Assignment(
    responsible="inter1",
    questionnaire_id="",
    quantity=5,
    identifying_data=d.dict())

res = AssignmentsApi(client).create(newobj)
```

Get list of interviews that were updated during last 15 minutes (using GraphQL)

```python
import datetime
from ssaw import InterviewApi

timestamp = datetime.datetime.now() - datetime.timedelta(minutes=15)
for i in InterviewsApi(client).get_list(update_date_gt=timestamp):
    print(i)
```

Get list of map files linked to the interviewer and remove the links

```python
from ssaw import MapsApi

for m in MapsApi(client).get_list(filter_user="inter"):
    print(m.file_name)
    MapsApi(client).delete_user(file_name=m.file_name, user_name="inter")
```
