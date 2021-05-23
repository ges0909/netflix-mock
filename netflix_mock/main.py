from logging.config import fileConfig
from pathlib import Path

import typer
import uvicorn

from netflix_mock.settings import get_settings


def main(env: Path = "../dev.env", log: Path = "../logging.conf"):
    if not env.exists():
        typer.echo(message=f"option '--env': application settings '{env}' not found", err=True)
        return
    if not log.exists():
        typer.echo(message=f"option '--log': log settings '{log}' not found", err=True)
        return
    settings = get_settings(app_config=env)
    fileConfig(fname=log, disable_existing_loggers=False)
    uvicorn.run(
        "netflix_mock.app:app",
        port=settings.server_port,
        log_level=settings.server_log_level,
        access_log=False,
        # reload=True,
    )


if __name__ == "__main__":
    typer.run(main)
