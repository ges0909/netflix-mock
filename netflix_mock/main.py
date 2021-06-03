from logging.config import fileConfig
from pathlib import Path
from typing import Tuple

import pydantic
import typer
import uvicorn

from netflix_mock.database import Database
from netflix_mock.settings import Settings


def has_suffix(path: Path, suffixes: Tuple[str, ...]) -> Path:
    if path.suffix in suffixes:
        return path
    raise typer.BadParameter(f"file '{path}' must have suffix '{suffixes}'")


def main(
    env_file: Path = typer.Option(
        ...,
        "--env",
        exists=True,
        callback=lambda path: has_suffix(path, (".env",)),
    ),
    config_file: Path = typer.Option(
        ...,
        "--config",
        exists=True,
        callback=lambda path: has_suffix(path, (".yml", ".yaml")),
    ),
):
    try:
        setattr(Settings.Config, "env_file", env_file)
        setattr(Settings.Config, "config_file", config_file)
        settings = Settings()
        fileConfig(
            fname=settings.logging.config,
            disable_existing_loggers=False,
        )
        _ = Database()  # drop/create database tables
        uvicorn.run(
            "netflix_mock.app:app",
            port=settings.server.port,
            log_level=settings.server.log_level,
            access_log=False,
            # reload=True,
        )
    except pydantic.ValidationError as error:
        raise typer.Exit(str(error))


if __name__ == "__main__":
    typer.run(main)
