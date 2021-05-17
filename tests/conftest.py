from base64 import b64encode

import pytest
from fastapi.testclient import TestClient

from main import app


@pytest.fixture(scope="session")
def client():
    return TestClient(app)


@pytest.fixture
def auth():
    return "Basic " + b64encode(b"test:test").decode("ascii")
