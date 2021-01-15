import json
import os
from pathlib import Path
import pytest

from dotenv import load_dotenv

from ssaw import Client


@pytest.fixture(scope="session", autouse=True)
def load_env_vars(request):
    curr_path = os.path.dirname(os.path.realpath(__file__))
    env_path = os.path.join(curr_path, "tests/env_vars.sh")
    load_dotenv(dotenv_path=env_path)
    env_path = os.path.join(curr_path, "tests/env_vars_override.sh")
    if os.path.isfile(env_path):
        load_dotenv(dotenv_path=env_path, override=True)

@pytest.fixture(scope="module")
def session():
    return Client(
        os.environ.get("base_url"),
        os.environ.get("SOLUTIONS_API_USER", ""),
        os.environ.get("SOLUTIONS_API_PASSWORD", ""))

@pytest.fixture(scope="module")
def params():
    return json.load(open("tests/params.json", mode="r"))
