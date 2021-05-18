from pathlib import Path
from typing import Any

from pydantic import BaseSettings


class Settings(BaseSettings):
    PORT: int = 9961
    BASIC_AUTH_USERNAME: str
    BASIC_AUTH_PASSWORD: str
    DATABASE_URL: str
    DATABASE_LOGGING: bool = False
    LOGGING_CONFIG: str = "logging.conf"
    TITLE: str
    DESCRIPTION: str

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


_settings = None


def get_settings(env_file=Path("../config/dev.env")):
    """ load settings only once"""
    global _settings
    if not _settings:
        if env_file and env_file.exists():
            _settings = Settings(_env_file=env_file)
    return _settings
