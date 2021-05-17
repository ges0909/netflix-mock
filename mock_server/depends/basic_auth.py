import secrets

import fastapi
from fastapi import Depends, HTTPException
from fastapi import status
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from mock_server.depends.app_settings import app_settings
from mock_server.settings import Settings

app = fastapi.FastAPI()
security = HTTPBasic()


def basic_auth(
    credentials: HTTPBasicCredentials = Depends(security),
    settings: Settings = Depends(app_settings),
):
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
