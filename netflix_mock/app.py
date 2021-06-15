from pathlib import Path

import fastapi
import pkg_resources
from fastapi.staticfiles import StaticFiles

from netflix_mock.database import create_database_model
from netflix_mock.middleware.catch_all import CatchAll
from netflix_mock.routers import (
    ef_ir,
    fake,
    home,
    settings,
    templates,
    todos,
    upload,
    users,
    video,
    weather,
)
from netflix_mock.ws.echo import echo

version = pkg_resources.get_distribution("netflix-mock").version

app = fastapi.FastAPI(
    title="Netflix Mock",
    description="Quick starter for mock server implementations.",
    version=version,
    docs_url="/docs",  # serves OpenAPI UI
    redoc_url=None,
    openapi_url="/api/openapi.json",
)

# mount static files
site_dir = Path(__file__).parent / ".." / "site"
if site_dir.exists():
    app.mount(path="/manual", app=StaticFiles(directory=site_dir))

# routers
app.include_router(router=home.router, include_in_schema=False)
app.include_router(router=templates.router, prefix="/templates", include_in_schema=False)
app.include_router(router=users.router, prefix="/api/users", tags=["Users"])
app.include_router(router=todos.router, prefix="/api/tasks", tags=["Todos"])
app.include_router(router=settings.router, prefix="/settings", tags=["Settings"])
app.include_router(router=weather.router, prefix="/weather", include_in_schema=False)
app.include_router(router=upload.router, tags=["Upload"])
app.include_router(router=fake.router, prefix="/fake", tags=["Fake Generator"])
app.include_router(router=ef_ir.router, prefix="/efir", tags=["EF-IR Mock"])
app.include_router(router=video.router, tags=["Streaming"])

# websocket
app.add_websocket_route(route=echo, path="/ws/echo")

# middleware
app.add_middleware(CatchAll)

# exception handlers
# app.add_exception_handler(exc_class_or_status_code=..., handler=...)


@app.on_event("startup")
async def startup():
    create_database_model()


@app.on_event("shutdown")
async def shutdown():
    """shutdown"""
