from pathlib import Path
from typing import Optional

from pydantic import BaseModel


class SettingsOut(BaseModel):
    server_port: Optional[int]
    server_log_level: Optional[str]
    basic_auth_username: Optional[str]
    database_url: Optional[str]
    database_logging: Optional[bool]
    upload_dir: Optional[Path]

    class Config:
        orm_mode = True
