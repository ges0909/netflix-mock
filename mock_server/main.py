from logging.config import fileConfig
from pathlib import Path
from typing import Optional

import typer
import uvicorn

from mock_server.config import get_settings


def main(config: Optional[Path] = None):
    env_file = config or Path("../dev.env")
    settings = get_settings(env_file=env_file)
    fileConfig(
        fname=settings.LOGGING_CONFIG,
        disable_existing_loggers=False,
    )
    uvicorn.run(
        "mock_server.app:app",
        port=settings.PORT,
        log_level="info",
        access_log=False,
        # reload=True,
    )


if __name__ == "__main__":
    typer.run(main)
