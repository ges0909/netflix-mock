from typing import Any

from pydantic import BaseSettings


class Settings(BaseSettings):
    PORT: int = 9961
    BASIC_AUTH_USERNAME: str
    BASIC_AUTH_PASSWORD: str
    DATABASE_URL: str
    DATABASE_LOGGING: bool = False
    LOGGING_CONFIG: str = "logging.conf"

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)


settings = Settings(_env_file="../dev.env")
