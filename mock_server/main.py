from logging.config import fileConfig
from pathlib import Path

import typer
import uvicorn

from mock_server.config import get_settings


def main(app_config: Path = "../dev.env", log_config: Path = "../logging.conf"):
    if not app_config.exists():
        typer.echo(
            message=f"option '--app-config': application config file '{app_config}' not found",
            err=True,
        )
        return
    if not log_config.exists():
        typer.echo(
            message=f"option '--log-config': logging config file '{log_config}' not found",
            err=True,
        )
        return
    settings = get_settings(app_config=app_config)
    fileConfig(fname=log_config, disable_existing_loggers=False)
    uvicorn.run(
        "mock_server.app:app",
        port=settings.PORT,
        log_level=settings.SERVER_LOG_LEVEL,
        access_log=False,
        # reload=True,
    )


if __name__ == "__main__":
    typer.run(main)
