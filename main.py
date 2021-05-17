import logging
import random
import string
import time
from pathlib import Path

import fastapi
import uvicorn
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles

from mock_server.database import Database
from mock_server.depends.app_settings import app_settings
from mock_server.routers import guide, weather, user, settings
from mock_server.views import home

app_root = Path(__file__).parent

app_settings = app_settings()

logging.config.fileConfig(
    fname=app_settings.LOGGING_CONF,
    disable_existing_loggers=False,
)

logger = logging.getLogger(__name__)

db = Database(app_settings=app_settings)

app = fastapi.FastAPI()

# mount static files
app.mount("/guide", StaticFiles(directory=str(app_root / "site")), name="guide")

# routers
app.include_router(home.router)
app.include_router(user.router, prefix="/users")
app.include_router(settings.router, prefix="/settings")
app.include_router(guide.router, prefix="/guide")
app.include_router(weather.router, prefix="/api")


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = "{0:.2f}".format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")

    return response


@app.on_event("startup")
async def startup():
    """models connect"""


@app.on_event("shutdown")
async def shutdown():
    """models disconnect"""


if __name__ == "__main__":
    uvicorn.run(app)
