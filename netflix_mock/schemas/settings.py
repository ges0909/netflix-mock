from pathlib import Path
from typing import Optional

from pydantic import BaseModel


class ServerOut(BaseModel):
    port: Optional[int]
    log_level: Optional[str]
    upload_dir: Optional[Path]


class DatabaseOut(BaseModel):
    url: Optional[str]
    logging: Optional[bool]


class LoggingOut(BaseModel):
    config: Optional[Path]


class MockOut(BaseModel):
    username: Optional[str]


class SettingsOut(BaseModel):
    server: Optional[ServerOut]
    database: Optional[DatabaseOut]
    logging: Optional[LoggingOut]
    mock: Optional[MockOut]

    class Config:
        orm_mode = True
