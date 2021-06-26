import os
import re
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Optional

# import yaml
import ruamel.yaml
import typer
from dotenv import load_dotenv
from pydantic import BaseModel, BaseSettings, validator
from ruamel.yaml import RoundTripLoader

# -- load yaml


env_var_pattern = re.compile(r".*(\${([\w]+)}).*")


def var_constructor(loader, node):
    """resolve environment variables while loading YAML files"""
    value = node.value
    match = env_var_pattern.match(value)
    env_var_name = match.group(2)  # 2 = inner group
    if env_var_value := os.environ.get(env_var_name):
        return value[: match.start(1)] + env_var_value + value[match.end(1) :]  # 1 = outer group
    raise typer.Exit(f"environment variable '{env_var_name}' not found")


# yaml.add_implicit_resolver("!env_var", env_var_pattern)
# yaml.add_constructor("!env_var", var_constructor)
ruamel.yaml.add_implicit_resolver("!env_var", env_var_pattern, Loader=RoundTripLoader)
ruamel.yaml.add_constructor("!env_var", var_constructor, Loader=RoundTripLoader)


def yaml_settings(settings: BaseSettings) -> Dict[str, Any]:
    env_file = getattr(settings.Config, "env_file", "dev.env")
    config_file = getattr(settings.Config, "config_file", "dev.yaml")
    load_dotenv(dotenv_path=env_file)
    with open(config_file, "r") as stream:
        # return yaml.load(stream, Loader=yaml.FullLoader)
        return ruamel.yaml.load(stream=stream, Loader=RoundTripLoader)


# -- models


class Template(BaseModel):
    dir: Path

    class Config:
        extra = "forbid"
        validate_assignment = True


class Upload(BaseModel):
    dir: Path

    class Config:
        extra = "forbid"
        validate_assignment = True

    @validator("dir")
    def exists(cls, v):
        if not v.exists():
            # v.mkdir(parents=True, exist_ok=True)
            raise ValueError(f"server upload dir '{v}' not found")

        return v


class Audio(BaseModel):
    dir: Path


class Video(BaseModel):
    dir: Path
    chunk_size: int = 1_048_576

    class Config:
        extra = "forbid"
        validate_assignment = True


class Server(BaseModel):
    port: int = 8000
    log_level: str
    template: Template
    upload: Upload
    audio: Audio
    video: Video

    class Config:
        extra = "forbid"
        validate_assignment = True


class Logging(BaseModel):
    config: Path

    class Config:
        extra = "forbid"
        validate_assignment = True

    @validator("config")
    def exists(cls, v):
        if not v.exists():
            raise ValueError(f"logging conf file '{v}' not found")
        return v


class Database(BaseModel):
    url: str
    logging: bool = False

    class Config:
        extra = "forbid"
        validate_assignment = True


class Api(BaseModel):
    username: str
    password: str
    spec: Optional[Path] = None

    class Config:
        extra = "forbid"
        validate_assignment = True

    @validator("spec")
    def exists(cls, v):
        if not v.exists():
            raise ValueError(f"open api spec file '{v}' not found")
        return v


class Admin(BaseModel):
    username: str
    password: str

    class Config:
        extra = "forbid"
        validate_assignment = True


class Settings(BaseSettings):
    server: Server
    logging: Logging
    database: Database
    api: Api
    admin: Admin

    class Config:
        extra = "forbid"
        validate_assignment = True

        @classmethod
        def customise_sources(
            cls,
            init_settings,
            env_settings,
            file_secret_settings,
        ):
            return (
                # init_settings,
                yaml_settings,
                # env_settings,
                # file_secret_settings,
            )


@lru_cache()
def get_settings():
    return Settings()
