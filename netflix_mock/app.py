import logging
from pathlib import Path

import fastapi
from fastapi import status
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from httpx import HTTPError
from sqlalchemy.exc import SQLAlchemyError

from netflix_mock.config import get_settings
from netflix_mock.routers import user, config, weather, guide, home
from netflix_mock.schemas.error import Error

logger = logging.getLogger(__name__)

settings = get_settings()
version = "0.14.9"  # pkg_resources.get_distribution("netflix-mock").version

app = fastapi.FastAPI(
    title=settings.OPENAPI_TITLE,
    description=settings.OPENAPI_DESCRIPTION,
    version=version,
)

# mount static files
site_dir = Path(__file__).parent / ".." / "site"
if site_dir.exists():
    app.mount("/guide", StaticFiles(directory=site_dir), name="guide")
    app.include_router(guide.router)

# routers
app.include_router(home.router)
app.include_router(user.router, prefix="/api/users")
app.include_router(config.router, prefix="/config")
app.include_router(weather.router, prefix="/weather")


@app.middleware("http")
async def handle_uncatched_exceptions(request: Request, call_next) -> Response:
    try:
        response = await call_next(request)
        return response
    except (HTTPError, SQLAlchemyError) as error:
        detail = ", ".join(error.args)
        return Response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=Error(detail=detail).json(),
            media_type="application/json",
        )


@app.on_event("startup")
async def startup():
    """models connect"""


@app.on_event("shutdown")
async def shutdown():
    """models disconnect"""
