# SSAW: Python wrapper for the Survey Solutions HTTP API

[![Python package](https://github.com/vavalomi/ssaw/workflows/Python%20package/badge.svg)](https://github.com/vavalomi/ssaw/actions)
[![codecov](https://codecov.io/gh/vavalomi/ssaw/branch/master/graph/badge.svg)](https://codecov.io/gh/vavalomi/ssaw)
[![PyPI version](https://badge.fury.io/py/ssaw.svg)](https://badge.fury.io/py/ssaw)
[![Documentation Status](https://readthedocs.org/projects/ssaw/badge/?version=latest)](https://ssaw.readthedocs.io/en/latest/?badge=latest)


SSAW is a Python library to access the [Survey Solutions API](<https://mysurvey.solutions>). This library enables you to manage resources such as creating assignments, users, maps; as well as perform workflow actions, like approving interviews, reassigning workspaces etc in your Python applications.


```python
import ssaw

# First, initialize connection with the server
client = ssaw.Client('https://demo.mysurvey.solutions', 'api_user', 'api_password')

# Get list of questionnaires
for q in ssaw.QuestionnairesApi(client).get_list():
    print(q.title)

# Download the latest exported data in SPSS format
filename = ssaw.ExportApi(client).get(export_type="SPSS",        
    questionnaire_identity="64136490cbc24a71a1df10f4b7115599$1")
```

Complete documentation at <https://ssaw.readthedocs.io>  
Details on API at <https://demo.mysurvey.solutions/apidocs>

Read more about Survey Solutions at <https://mysurvey.solutions>