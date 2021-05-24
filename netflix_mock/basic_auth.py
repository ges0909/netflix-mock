import secrets

from fastapi import Depends, HTTPException
from fastapi import status
from fastapi.security import HTTPBasicCredentials, HTTPBasic

from netflix_mock.settings import Settings

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


settings = Settings()
mock_user = BasicAuth(username=settings.mock_username, password=settings.mock_password)
admin_user = BasicAuth(username=settings.admin_username, password=settings.admin_password)
