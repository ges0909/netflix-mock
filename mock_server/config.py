from pathlib import Path
from typing import Any, Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    PORT: int = 9961
    BASIC_AUTH_USERNAME: str
    BASIC_AUTH_PASSWORD: str
    DATABASE_URL: str
    DATABASE_LOGGING: bool = False
    LOGGING_CONFIG: str = "logging.conf"
    OPENAPI_TITLE: str
    OPENAPI_DESCRIPTION: str

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


_settings: Optional[Settings] = None


def get_settings(config_file=Path("../config/dev.env")):
    """load settings only once"""
    global _settings
    if not _settings:
        if config_file and config_file.exists():
            _settings = Settings(_env_file=config_file)
    return _settings
