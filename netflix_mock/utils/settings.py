import os
import re
from pathlib import Path
from typing import Any, Dict, Optional

import pydantic.main
import yaml
from dotenv import load_dotenv
from pydantic import BaseModel, BaseSettings, validator

from netflix_mock.utils.singleton import Singleton

var_matcher = re.compile(r".*\$\{([\w]+)\}.*")


def var_constructor(loader, node):
    """extract the matched value, expand env variable, and replace the match"""
    value = node.value
    match = var_matcher.match(value)
    var = match.group(1)
    val = os.environ.get(var)
    return value.replace(f"${{{var}}}", val)


yaml.add_implicit_resolver("!var", var_matcher)
yaml.add_constructor("!var", var_constructor)


def yaml_settings(settings: BaseSettings) -> Dict[str, Any]:
    load_dotenv(dotenv_path="../dev.env")
    config_file = getattr(settings.Config, "config_file")
    with open(config_file, "r") as stream:
        return yaml.load(stream, Loader=yaml.FullLoader)


class Server(BaseModel):
    port: int = 8000
    log_level: str
    upload_dir: Path


class Logging(BaseModel):
    config: Path

    @validator("config")
    def logging_conf_file_exists(cls, v):
        if not v or not v.exists():
            raise ValueError(f"logging conf file '{v}' not found")
        return v


class Database(BaseModel):
    url: str
    logging: bool = False
    drop_tables: bool = False


class Mock(BaseModel):
    username: str
    password: str
    open_api: Optional[Path] = None

    @validator("open_api")
    def open_api_spec_exists(cls, v):
        if v and not v.exists():
            raise ValueError(f"open api spec file '{v}' not found")
        return v


class Admin(BaseModel):
    username: str
    password: str


class CombinedMetaClasses(pydantic.main.ModelMetaclass, Singleton):
    pass


class Settings(BaseSettings, metaclass=CombinedMetaClasses):
    server: Server
    logging: Logging
    database: Database
    mock: Mock
    admin: Admin

    class Config:
        validate_assignment = True

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (
                init_settings,
                yaml_settings,
                env_settings,
                file_secret_settings,
            )
