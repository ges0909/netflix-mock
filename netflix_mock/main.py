from logging.config import fileConfig
from pathlib import Path

import typer
import uvicorn

from netflix_mock.utils.database import Database
from netflix_mock.utils.settings import Settings


def main(
    env_file: Path = typer.Option(..., "--env", exists=True),
    config_file: Path = typer.Option(..., "--config", exists=True),
):
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


if __name__ == "__main__":
    typer.run(main)
