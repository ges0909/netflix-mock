import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from netflix_mock.common.settings import Settings

security = HTTPBasic()


class BasicAuth:
    def __init__(self, username: str, password: str):
        self._username = username
        self._password = password

    def __call__(self, credentials: HTTPBasicCredentials = Depends(security)) -> None:
        correct_username = secrets.compare_digest(credentials.username, self._username)
        correct_password = secrets.compare_digest(credentials.password, self._password)
        if not (correct_username and correct_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="incorrect username or password",
                headers={"WWW-Authenticate": "Basic"},
            )


settings = Settings()

mock_user = BasicAuth(username=settings.api.username, password=settings.api.password)
admin_user = BasicAuth(username=settings.admin.username, password=settings.admin.password)
