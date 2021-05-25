from pathlib import Path

import fastapi
import pkg_resources
from fastapi.staticfiles import StaticFiles

from netflix_mock.middleware.uncaught_exceptions import UncaughtExceptions
from netflix_mock.routers import users, settings, weather, templates, upload, home
from netflix_mock.ws.echo import echo

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
app.include_router(router=home.router, include_in_schema=False)
app.include_router(router=templates.router, prefix="/templates", include_in_schema=False)
app.include_router(router=users.router, prefix="/api/users", tags=["Users"])
app.include_router(router=settings.router, prefix="/settings", tags=["Settings"])
app.include_router(router=weather.router, prefix="/weather", include_in_schema=False)
app.include_router(router=upload.router, tags=["Upload"])

# websocket
app.add_websocket_route(route=echo, path="/ws/echo")

# middleware
app.add_middleware(UncaughtExceptions)


@app.on_event("startup")
async def startup():
    """models connect"""


@app.on_event("shutdown")
async def shutdown():
    """models disconnect"""
