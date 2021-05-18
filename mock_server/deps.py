import secrets
from functools import lru_cache

import fastapi
from fastapi import Depends, HTTPException
from fastapi import status
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from mock_server.config import Settings, settings

app = fastapi.FastAPI()
security = HTTPBasic()


@lru_cache()
def get_settings() -> Settings:
    return settings


def get_basic_auth(
    credentials: HTTPBasicCredentials = Depends(security),
    settings_: Settings = Depends(get_settings),
):
    correct_username = secrets.compare_digest(
        credentials.username,
        settings_.BASIC_AUTH_USERNAME,
    )
    correct_password = secrets.compare_digest(
        credentials.password,
        settings_.BASIC_AUTH_PASSWORD,
    )
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username


def get_db_session():
    from mock_server.main import db

    with db.SessionLocal() as sess:
        yield sess
