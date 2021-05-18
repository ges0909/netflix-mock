from logging.config import fileConfig
from pathlib import Path
from typing import Optional

import typer
import uvicorn

from mock_server.config import get_settings

settings = get_settings()

fileConfig(
    fname=settings.LOGGING_CONFIG,
    disable_existing_loggers=False,
)


def main(dotenv: Optional[Path] = None):
    # env_file = dotenv or "../dev.env"
    # settings = Settings(_env_file=env_file)
    uvicorn.run(
        "mock_server.app:app",
        port=settings.PORT,
        log_level="info",
        access_log=False,
        # reload=True,
    )


if __name__ == "__main__":
    typer.run(main)
