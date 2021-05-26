from logging.config import fileConfig
from pathlib import Path

import typer
import uvicorn

from netflix_mock.settings import Settings


def main(config: Path = "dev.env"):
    if not config.exists():
        typer.echo(message=f"option '--config': application config file '{config}' not found", err=True)
        return
    settings = Settings(env_file=config)
    fileConfig(
        fname=settings.logging_conf,
        disable_existing_loggers=False,
    )
    uvicorn.run(
        "netflix_mock.app:app",
        port=settings.server_port,
        log_level=settings.server_log_level,
        access_log=False,
        # reload=True,
    )


if __name__ == "__main__":
    typer.run(main)
