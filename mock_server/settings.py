from pathlib import Path
from typing import Any

from pydantic import BaseSettings


class Settings(BaseSettings):
    PORT: int = 9961
    DATABASE_URL: str
    BASIC_AUTH_USERNAME: str
    BASIC_AUTH_PASSWORD: str
    LOGGING_CONF: Path = Path.home() / "logging.conf"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)
