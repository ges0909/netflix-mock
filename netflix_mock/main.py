from logging.config import fileConfig
from pathlib import Path

import typer
import uvicorn

from netflix_mock.utils.database import Database
from netflix_mock.utils.settings import Settings


def main(config: Path = "dev.env"):
    if not config.exists():
        typer.echo(message=f"option '--config': application config file '{config}' not found", err=True)
        return
    setattr(Settings.Config, "config_file", config)
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
