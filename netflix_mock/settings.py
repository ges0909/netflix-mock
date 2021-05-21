from pathlib import Path
from typing import Any, Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    SERVER_PORT: int = 9961
    SERVER_LOG_LEVEL: str
    BASIC_AUTH_USERNAME: str
    BASIC_AUTH_PASSWORD: str
    DATABASE_URL: str
    DATABASE_LOGGING: bool = False

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


_settings: Optional[Settings] = None


def get_settings(app_config=Path("../dev.env")) -> Settings:
    global _settings
    if not _settings:  # load settings only once
        if app_config and app_config.exists():
            _settings = Settings(_env_file=app_config)
    return _settings
