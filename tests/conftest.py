from base64 import b64encode

import pytest
from faker import Faker
from fastapi.testclient import TestClient

from netflix_mock.app import app
from netflix_mock.settings import get_settings

fake = Faker()


@pytest.fixture
def settings():
    return get_settings()


@pytest.fixture
def client(settings, tmp_path):
    db_file = tmp_path / "test.db"
    client = TestClient(app)
    settings.database_url = f"sqlite:///{db_file}"
    settings.upload_dir = tmp_path
    return client


@pytest.fixture
def mock_user():
    return "Basic " + b64encode(b"test:test").decode("ascii")


@pytest.fixture
def admin_user():
    return "Basic " + b64encode(b"admin:admin").decode("ascii")


@pytest.fixture
def user():
    return dict(
        username=fake.pystr(min_chars=8, max_chars=16),
        password=fake.pystr(min_chars=8, max_chars=64),
    )
