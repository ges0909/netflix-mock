from pathlib import Path
from typing import Any, Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    server_port: int = 9961
    server_log_level: str
    database_url: str
    database_logging: bool = False
    upload_dir: Path
    mock_username: str
    mock_password: str
    admin_username: str
    admin_password: str

    class Config:
        validate_assignment = True


_settings: Optional[Settings] = None


def get_settings(app_config=Path("../dev.env")) -> Settings:
    global _settings
    if not _settings:  # load settings only once
        if app_config and app_config.exists():
            _settings = Settings(_env_file=app_config)
    return _settings
