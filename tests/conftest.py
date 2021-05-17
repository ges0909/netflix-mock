from base64 import b64encode

import pytest
from fastapi.testclient import TestClient

from main import app
from mock_server.config import Settings


@pytest.fixture
def test_client(monkeypatch):
    Settings._env_file = "../dev.env"
    monkeypatch.setenv("LOGGING_CONF", "../logging.conf")
    return TestClient(app)


@pytest.fixture
def basic_auth():
    return "Basic " + b64encode(b"test:test").decode("ascii")
