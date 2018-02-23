import os
import pytest
import ssaw

@pytest.fixture(scope="module")
def session():
	API_USER = os.environ.get('SOLUTIONS_API_USER', None)
	API_PASSWORD = os.environ.get('SOLUTIONS_API_PASSWORD', None)
	ss = ssaw.init('https://demo.mysurvey.solutions/', API_USER, API_PASSWORD)
	return ss

@pytest.fixture(scope="module")
def params():
	return {
		'QuestionnaireId': '2b94af4c-c360-4fcb-a511-4374dfe0d363$1',
		'TemplateId': '2b94af4c-c360-4fcb-a511-4374dfe0d363',
		'TemplateVersion': 1,
		'InterviewId': '778ac633-73b3-40df-a6fe-799f0e235804'
	}
