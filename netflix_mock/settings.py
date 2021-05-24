from pathlib import Path
from typing import Any

from pydantic import BaseSettings


class Settings(BaseSettings):
    server_port: int = 8000
    server_log_level: str
    database_url: str
    database_logging: bool = False
    upload_dir: Path
    mock_username: str
    mock_password: str
    admin_username: str
    admin_password: str

    __instance = None
    __initialized = False

    class Config:
        validate_assignment = True

    # mimic singleton with args

    def __new__(cls, *args, **kwargs):
        if not Settings.__instance:
            Settings.__instance = object.__new__(cls)
        return Settings.__instance

    def __init__(self, env_file=Path("../dev.env"), **values: Any):
        if not Settings.__initialized:
            super().__init__(_env_file=env_file, **values)
            Settings.__initialized = True
