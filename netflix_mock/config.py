from pathlib import Path
from typing import Any, Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    PORT: int = 9961
    BASIC_AUTH_USERNAME: str
    BASIC_AUTH_PASSWORD: str
    DATABASE_URL: str
    DATABASE_LOGGING: bool = False
    OPENAPI_TITLE: str
    OPENAPI_DESCRIPTION: str
    SERVER_LOG_LEVEL: str

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


_settings: Optional[Settings] = None


def get_settings(app_config=Path("../dev.env")):
    """load settings only once"""
    global _settings
    if not _settings:
        if app_config and app_config.exists():
            _settings = Settings(_env_file=app_config)
    return _settings
