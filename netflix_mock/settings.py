from pathlib import Path
from typing import Any

from pydantic import BaseSettings


class Settings(BaseSettings):
    server_port: int = 8000
    server_log_level: str
    database_url: str
    database_logging: bool = False
    logging_conf: Path
    upload_dir: Path
    mock_username: str
    mock_password: str
    admin_username: str
    admin_password: str

    _instance = None

    class Config:
        validate_assignment = True

    def __new__(cls, env_file=None, *args, **kwargs):
        if env_file:
            Settings._instance = object.__new__(cls)
        return Settings._instance

    def __init__(self, env_file=None, **values: Any):
        if env_file:
            super().__init__(_env_file=env_file, **values)
