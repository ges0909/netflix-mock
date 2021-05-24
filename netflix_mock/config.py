from pathlib import Path
from typing import Any

from pydantic import BaseSettings


class Config(BaseSettings):
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

    def __new__(cls, config=None, *args, **kwargs):
        if config:
            Config._instance = object.__new__(cls)
        return Config._instance

    def __init__(self, config=None, **values: Any):
        if config:
            super().__init__(_env_file=config, **values)
