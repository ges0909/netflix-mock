from pathlib import Path
from typing import Optional

from pydantic import BaseModel


class Server(BaseModel):
    port: Optional[int]
    log_level: Optional[str]
    upload_dir: Optional[Path]


class Database(BaseModel):
    url: Optional[str]
    logging: Optional[bool]


class Logging(BaseModel):
    config: Optional[Path]


class Mock(BaseModel):
    username: Optional[str]


class SettingsOut(BaseModel):
    server: Optional[Server]
    database: Optional[Database]
    logging: Optional[Logging]
    mock: Optional[Mock]

    class Config:
        orm_mode = True
