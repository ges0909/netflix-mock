from pathlib import Path
from typing import Any, Optional

from pydantic import BaseSettings, validator
from pydantic.main import ModelMetaclass

from netflix_mock.utils.singleton import Singleton


class CombinedClass(ModelMetaclass, Singleton):
    pass


class Settings(BaseSettings, metaclass=CombinedClass):
    server_port: int = 8000
    server_log_level: str
    logging_conf: Path
    database_url: str
    database_logging: bool = False
    database_drop_tables: bool = False
    upload_dir: Path
    er_if_open_api_spec: Optional[Path] = None
    mock_username: str
    mock_password: str
    admin_username: str
    admin_password: str

    class Config:
        validate_assignment = True

    @validator("logging_conf")
    def logging_conf_file_exists(cls, v):
        if not v or not v.exists():
            raise ValueError(f"logging conf file '{v}' not found")
        return v

    @validator("er_if_open_api_spec")
    def open_api_spec_exists(cls, v):
        if v and not v.exists():
            raise ValueError(f"open api spec file '{v}' not found")
        return v

    def __init__(self, env_file=None, **values: Any):
        if env_file:
            super().__init__(_env_file=env_file, **values)
