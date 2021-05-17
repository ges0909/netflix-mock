from pathlib import Path
from typing import Any

from pydantic import BaseSettings


class Settings(BaseSettings):
    PORT: int = 9961
    DATABASE_URL: str
    BASIC_AUTH_USERNAME: str
    BASIC_AUTH_PASSWORD: str
    LOGGING_CONF: str = Path.home() / "logging.conf"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


settings = Settings(_env_file="dev.env")
