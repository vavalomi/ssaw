import os
import pytest
from ssaw.headquarters import Headquarters

@pytest.fixture(scope="module")
def session():
    API_USER = os.environ.get('SOLUTIONS_API_USER', None)
    API_PASSWORD = os.environ.get('SOLUTIONS_API_PASSWORD', None)
    ss = Headquarters('https://apitest.mysurvey.solutions/', API_USER, API_PASSWORD)
    return ss

@pytest.fixture(scope="module")
def params():
    return {
        'QuestionnaireId': 'ecb715a3-e856-48d7-9f81-35dc3bb6a301$1',
        'TemplateId': 'ecb715a3-e856-48d7-9f81-35dc3bb6a301',
        'TemplateVersion': 1,
        'InterviewId': 'fdd62d6c-c8a3-4737-ac76-26125f0b9d82',
        'SupervisorId': 'b252a359-00e6-4605-b642-a4094d8db8d7',
        'InterviewerId': ''
    }
