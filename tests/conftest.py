from base64 import b64encode

import pytest
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from netflix_mock.settings import Settings

fake = Faker()


@pytest.fixture
def settings(tmp_path):
    Settings.Config.env_file = "config/test.env"
    Settings.Config.config_file = "config/test.yaml"
    settings = Settings()
    settings.server.upload_dir = tmp_path
    return settings


@pytest.fixture
def db_session(settings):
    from netflix_mock.database import Base
    from netflix_mock.models.todo import Todo
    from netflix_mock.models.user import User

    _ = User()
    _ = Todo()

    engine = create_engine(
        settings.database.url,
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(bind=engine)
    with engine.begin() as conn:
        Base.metadata.create_all(bind=conn)
    return sessionmaker(
        # autocommit=False,
        autoflush=False,
        bind=engine,
    )


@pytest.fixture
def client(settings, db_session):
    from netflix_mock.app import app
    from netflix_mock.database import get_session

    def override_get_session():
        with db_session() as session:
            yield session

    client = TestClient(app)
    app.dependency_overrides[get_session] = override_get_session

    return client


@pytest.fixture
def api_user():
    return "Basic " + b64encode(b"test:test").decode("ascii")


@pytest.fixture
def admin_user():
    return "Basic " + b64encode(b"admin:admin").decode("ascii")


@pytest.fixture
def user_data():
    profile = fake.profile()
    name = profile["name"].split()
    return dict(
        username=profile["username"],
        password=fake.pystr(min_chars=8, max_chars=16),
        email=profile["mail"],
        first_name=name[0],
        last_name=name[1],
    )
