from logging.config import fileConfig
from pathlib import Path

import typer
import uvicorn

from netflix_mock.settings import Settings


def main(config: Path = "../dev.env"):
    if not config.exists():
        typer.echo(message=f"option '--config': application config file '{config}' not found", err=True)
        return
    config_ = Settings(config=config)
    fileConfig(
        fname=config_.logging_conf,
        disable_existing_loggers=False,
    )
    uvicorn.run(
        "netflix_mock.app:app",
        port=config_.server_port,
        log_level=config_.server_log_level,
        access_log=False,
        # reload=True,
    )


if __name__ == "__main__":
    typer.run(main)
