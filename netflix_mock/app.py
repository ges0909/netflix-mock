import logging
from pathlib import Path

import fastapi
from fastapi.staticfiles import StaticFiles

from netflix_mock.routers import users, settings, weather, home, upload
from netflix_mock.settings import get_settings

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
    app.mount("/manual", StaticFiles(directory=site_dir))

# routers
app.include_router(home.router, include_in_schema=False)
app.include_router(users.router, prefix="/api/users", tags=["Get, add, update and delete users"])
app.include_router(settings.router, prefix="/settings", include_in_schema=False)
app.include_router(weather.router, prefix="/weather", include_in_schema=False)
app.include_router(upload.router, tags=["Upload file(s)"])


@app.on_event("startup")
async def startup():
    """models connect"""


@app.on_event("shutdown")
async def shutdown():
    """models disconnect"""
