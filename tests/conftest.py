from base64 import b64encode

import pytest
from faker import Faker
from fastapi.testclient import TestClient

from netflix_mock.utils.settings import Settings

fake = Faker()


@pytest.fixture
def settings():
    Settings.Config.env_file = "../dev.env"
    Settings.Config.config_file = "../dev.yaml"
    return Settings()


@pytest.fixture
def client(settings, tmp_path):
    from netflix_mock.app import app

    client = TestClient(app)
    settings.database.url = f"sqlite:///{tmp_path / 'test.db'}"
    settings.server.upload_dir = tmp_path

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
