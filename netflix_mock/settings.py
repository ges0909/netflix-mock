from pathlib import Path
from typing import Any, Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    server_port: int = 8000
    server_log_level: str
    logging_conf: Path
    database_url: str
    database_logging: bool = False
    upload_dir: Path
    er_if_open_api_spec: Optional[Path] = None
    mock_username: str
    mock_password: str
    admin_username: str
    admin_password: str

    _instance = None

    class Config:
        validate_assignment = True

    def __new__(cls, config=None, *args, **kwargs):
        if config:
            Settings._instance = object.__new__(cls)
        return Settings._instance

    def __init__(self, config=None, **values: Any):
        if config:
            super().__init__(_env_file=config, **values)
