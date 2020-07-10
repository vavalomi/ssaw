# SSAW: Python wrapper for the Survey Solutions HTTP API

[![Build Status](https://travis-ci.org/vavalomi/ssaw.svg?branch=master)](https://travis-ci.org/vavalomi/ssaw)
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
from ssaw import AssignmentsApi

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
```

Get list of interviews that were updated during last 15 minutes (using GraphQL)
```python
import datetime
from ssaw import InterviewApi

timestamp = datetime.datetime.now() - datetime.timedelta(minutes=15)
for i in InterviewsApi(client).get_list(update_date_gt=timestamp):
    print(i)
```