import secrets

from fastapi import Depends, HTTPException
from fastapi import status
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from mock_server.config import settings

security = HTTPBasic()


def get_basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(
        credentials.username,
        settings.BASIC_AUTH_USERNAME,
    )
    correct_password = secrets.compare_digest(
        credentials.password,
        settings.BASIC_AUTH_PASSWORD,
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
