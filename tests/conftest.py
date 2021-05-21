from base64 import b64encode

import pytest
from faker import Faker
from fastapi.testclient import TestClient

from netflix_mock.app import app
from netflix_mock.settings import get_settings

fake = Faker()


@pytest.fixture
def client(tmp_path):
    db_file = tmp_path / "test.db"
    client = TestClient(app)
    settings = get_settings()
    settings.DATABASE_URL = f"sqlite:///{db_file}"
    return client


@pytest.fixture
def basic_auth():
    return "Basic " + b64encode(b"test:test").decode("ascii")


@pytest.fixture
def user():
    return dict(
        username=fake.pystr(min_chars=8, max_chars=16),
        password=fake.pystr(min_chars=8, max_chars=64),
    )
