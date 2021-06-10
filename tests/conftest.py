from base64 import b64encode

import pytest
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from netflix_mock.database import Base, Database
from netflix_mock.settings import Settings

fake = Faker()


# def override_get_db():
#     with TestingSessionLocal() as db:
#         yield db


@pytest.fixture
def settings():
    Settings.Config.env_file = "test.env"
    Settings.Config.config_file = "test.yaml"
    return Settings()


# @pytest.fixture
# def session(settings):
#     engine = create_engine(
#         settings.database.url,
#         connect_args={"check_same_thread": False},
#     )
#     Base.metadata.create_all(bind=engine)
#     return sessionmaker(
#         # autocommit=False,
#         autoflush=False,
#         bind=engine,
#     )


@pytest.fixture
def client(settings, tmp_path):
    from netflix_mock.app import app

    client = TestClient(app)
    # app.dependency_overrides[session] = override_get_db
    # settings.database.url = f"sqlite:///{tmp_path / 'test.db'}"
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
    profile = fake.profile()
    name = profile["name"].split()
    return dict(
        username=profile["username"],
        password=fake.pystr(min_chars=8, max_chars=16),
        email=profile["mail"],
        first_name=name[0],
        last_name=name[1],
    )
