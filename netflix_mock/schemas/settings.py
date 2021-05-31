from pathlib import Path
from typing import Optional

from pydantic import BaseModel, SecretStr


class ServerOut(BaseModel):
    port: Optional[int]
    log_level: Optional[str]
    upload_dir: Optional[Path]


class DatabaseOut(BaseModel):
    url: Optional[str]
    logging: Optional[bool]


class LoggingOut(BaseModel):
    config: Optional[Path]


class ApiOut(BaseModel):
    username: Optional[str]
    password: Optional[SecretStr]


class SettingsOut(BaseModel):
    server: Optional[ServerOut]
    database: Optional[DatabaseOut]
    logging: Optional[LoggingOut]
    api: Optional[ApiOut]

    class Config:
        orm_mode = True
