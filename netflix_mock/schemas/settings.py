from pathlib import Path
from typing import Optional

from pydantic import BaseModel, SecretStr


class TemplateOut(BaseModel):
    dir: Path


class UploadOut(BaseModel):
    dir: Path


class VideoOut(BaseModel):
    dir: Path
    chunk_size: int


class ServerOut(BaseModel):
    port: Optional[int]
    log_level: Optional[str]
    template: Optional[TemplateOut]
    upload: Optional[UploadOut]
    video: Optional[VideoOut]


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
