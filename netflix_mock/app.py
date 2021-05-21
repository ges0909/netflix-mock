import logging
from pathlib import Path

import fastapi
from fastapi import status
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from httpx import HTTPError
from sqlalchemy.exc import SQLAlchemyError

from netflix_mock.settings import get_settings
from netflix_mock.routers import users, settings, weather, guide, home, files
from netflix_mock.schemas.error import Error

logger = logging.getLogger(__name__)

settings_ = get_settings()
version = "0.14.9"  # pkg_resources.get_distribution("netflix-mock").version

app = fastapi.FastAPI(
    title="Netflix Mock with FastAPI",
    description="A configurable quick starter for mock server implementations.",
    version=version,
)

# mount static files
site_dir = Path(__file__).parent / ".." / "site"
if site_dir.exists():
    app.mount("/guide", StaticFiles(directory=site_dir), name="guide")
    app.include_router(guide.router, include_in_schema=False)

# routers
app.include_router(home.router, include_in_schema=False)
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(settings.router, prefix="/settings", include_in_schema=False)
app.include_router(weather.router, prefix="/weather", include_in_schema=False)
app.include_router(files.router, prefix="/files", tags=["Files"])


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
