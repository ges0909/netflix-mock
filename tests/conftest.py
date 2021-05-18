from base64 import b64encode

import pytest
from fastapi.testclient import TestClient

from mock_server.main import app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def basic_auth():
    return "Basic " + b64encode(b"test:test").decode("ascii")
