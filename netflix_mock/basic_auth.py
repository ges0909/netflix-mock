import secrets

from fastapi import Depends, HTTPException
from fastapi import status
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from netflix_mock.config import Config

security = HTTPBasic()


class BasicAuth:
    def __init__(self, username: str, password: str):
        self._username = username
        self._password = password

    def __call__(self, credentials: HTTPBasicCredentials = Depends(security)) -> bool:
        correct_username = secrets.compare_digest(credentials.username, self._username)
        correct_password = secrets.compare_digest(credentials.password, self._password)
        if correct_username and correct_password:
            return True
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )


config = Config()

mock_user = BasicAuth(username=config.mock_username, password=config.mock_password)
admin_user = BasicAuth(username=config.admin_username, password=config.admin_password)
