import logging
import random
import string
import time
from logging.config import fileConfig
from pathlib import Path
from typing import Optional

import fastapi
import typer
import uvicorn
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles

from mock_server.config import settings
from mock_server.db import Database
from mock_server.routers import user, config, weather, guide, home

fileConfig(
    fname=settings.LOGGING_CONFIG,
    disable_existing_loggers=False,
)

logger = logging.getLogger(__name__)

db = Database(settings=settings)

app = fastapi.FastAPI()

# mount static files
app.mount("/guide", StaticFiles(directory="../site"), name="guide")

# routers
app.include_router(home.router)
app.include_router(user.router, prefix="/users")
app.include_router(weather.router, prefix="/api")
app.include_router(config.router)
app.include_router(guide.router)


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)
    logger.info(f"rid={idem} completed in={formatted_process_time}ms status_code={response.status_code}")

    return response


@app.on_event("startup")
async def startup():
    """models connect"""


@app.on_event("shutdown")
async def shutdown():
    """models disconnect"""


def main(dotenv: Optional[Path] = None):
    # env_file = dotenv or "../dev.env"
    # settings = Settings(_env_file=dotenv or "../dev.env")
    uvicorn.run(app)


if __name__ == "__main__":
    typer.run(main)
