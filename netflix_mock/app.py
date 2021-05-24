from pathlib import Path

import fastapi
import pkg_resources
from fastapi.staticfiles import StaticFiles

from netflix_mock.middleware.uncaught_exceptions import UncaughtExceptions
from netflix_mock.routers import users, settings, weather, templates, upload, home

version = pkg_resources.get_distribution("netflix-mock").version

app = fastapi.FastAPI(
    title="Netflix Mock",
    description="A configurable quick starter for mock server implementations.",
    version=version,
    openapi_url="/api/openapi.json",
    # docs_url="/docs",
    redoc_url=None,
)

# mount static files
site_dir = Path(__file__).parent / ".." / "site"
if site_dir.exists():
    app.mount("/manual", StaticFiles(directory=site_dir))

# routers
app.include_router(home.router, include_in_schema=False)
app.include_router(templates.router, prefix="/templates", include_in_schema=False)
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(settings.router, prefix="/settings", tags=["Settings"])
app.include_router(weather.router, prefix="/weather", include_in_schema=False)
app.include_router(upload.router, tags=["Upload"])

# middleware
app.add_middleware(UncaughtExceptions)


@app.on_event("startup")
async def startup():
    """models connect"""


@app.on_event("shutdown")
async def shutdown():
    """models disconnect"""
