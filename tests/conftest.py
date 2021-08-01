from base64 import b64encode
from pathlib import Path
from typing import Any

import pytest
from faker import Faker
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from netflix_mock.settings import Settings, get_settings

fake = Faker()


@pytest.fixture
def upload_dir(tmp_path) -> Path:
    upload_dir_ = tmp_path / "uploads"
    upload_dir_.mkdir()
    return upload_dir_


@pytest.fixture
def settings(tmp_path, upload_dir) -> Settings:
    env_config = r"""
    HOME = "${USERPROFILE}" # windows only

    MOCK_USERNAME = "test"
    MOCK_PASSWORD = "test"

    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "admin"
    """

    app_config = f"""
    server:
      port: 8000
      log_level: debug  # critical, error, warning, info, debug, trace
      template:
        dir: templates
      upload:
        dir: {upload_dir}
      audio:
        dir: audio
      video:
        dir: video

    logging:
      config: ${{HOME}}/Projekte/netflix-mock/logging.conf

    database:
      url: 'sqlite+pysqlite:///:memory:'
      logging: true

    api:
      username: ${{MOCK_USERNAME}}  # basic auth
      password: ${{MOCK_PASSWORD}}  # basic auth
      spec: ${{HOME}}/Projekte/netflix-mock/er-if.json

    admin:
      username: ${{ADMIN_USERNAME}} # basic auth to change settings
      password: ${{ADMIN_USERNAME}} # basic auth to change settings
    """

    Settings.Config.env_file = tmp_path / "test.env"
    Settings.Config.config_file = tmp_path / "test.yaml"

    with open(Settings.Config.env_file, "w") as stream:
        stream.write(env_config)
    with open(Settings.Config.config_file, "w") as stream:
        stream.write(app_config)

    settings = get_settings()
    settings.server.upload.dir = upload_dir

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
def client(settings, db_session) -> TestClient:
    from netflix_mock.app import app
    from netflix_mock.database import get_db_session

    def override_get_db_session():
        with db_session() as session:
            yield session

    client = TestClient(app)
    app.dependency_overrides[get_db_session] = override_get_db_session

    return client


@pytest.fixture
def api_user() -> str:
    return "Basic " + b64encode(b"test:test").decode("ascii")


@pytest.fixture
def admin_user() -> str:
    return "Basic " + b64encode(b"admin:admin").decode("ascii")


@pytest.fixture
def fake_user() -> dict[str, Any]:
    profile = fake.profile()
    name = profile["name"].split()
    return dict(
        username=profile["username"],
        password=fake.pystr(min_chars=8, max_chars=16),
        email=profile["mail"],
        first_name=name[0],
        last_name=name[1],
    )
