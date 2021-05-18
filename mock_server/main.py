import logging
from logging.config import fileConfig
from pathlib import Path
from typing import Optional

import typer
import uvicorn

from mock_server.config import settings
from mock_server.db import Database

fileConfig(
    fname=settings.LOGGING_CONFIG,
    disable_existing_loggers=False,
)

logger = logging.getLogger(__name__)

db = Database(settings=settings)


def main(dotenv: Optional[Path] = None):
    # env_file = dotenv or "../dev.env"
    # settings = Settings(_env_file=env_file)
    from mock_server.app import app
    uvicorn.run(app)


if __name__ == "__main__":
    typer.run(main)
