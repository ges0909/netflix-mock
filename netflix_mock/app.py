import importlib.metadata as importlib_metadata
from pathlib import Path

import fastapi
from fastapi import Depends
from fastapi.staticfiles import StaticFiles

from netflix_mock.database import create_database_model
from netflix_mock.depends.basic_auth import admin_user, api_user
from netflix_mock.middleware.catch_all import CatchAll
from netflix_mock.middleware.http_logging import HttpLogging
from netflix_mock.routers import (
    audio,
    catch_all,
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
from netflix_mock.websocket.echo import echo

version = importlib_metadata.version("netflix_mock")

app = fastapi.FastAPI(
    title="Netflix Mock",
    description="Quick starter for mock server implementations.",
    version=f"v{version}",
    # docs_url="/docs",  # serves OpenAPI UI
    redoc_url=None,
    openapi_url="/api/openapi.json",
    # dependencies=[Depends(api_user)],  # apply to all path operations
)

# mount static files
site_dir = Path(__file__).parent / ".." / "site"
if site_dir.exists():
    app.mount(path="/manual", app=StaticFiles(directory=site_dir))

# routers


app.include_router(
    router=home.router,
    include_in_schema=False,
)
app.include_router(
    router=templates.router,
    prefix="/templates",
    include_in_schema=False,
)
app.include_router(
    router=users.router,
    prefix="/api/users",
    tags=["Users"],
    dependencies=[Depends(api_user)],
)
app.include_router(
    router=todos.router,
    prefix="/api/tasks",
    tags=["Todos"],
    dependencies=[Depends(api_user)],
)
app.include_router(
    router=settings.router,
    prefix="/settings",
    tags=["Settings"],
    dependencies=[Depends(admin_user)],
)
app.include_router(
    router=weather.router,
    prefix="/weather",
    include_in_schema=False,
)
app.include_router(
    router=upload.router,
    tags=["Upload"],
)
app.include_router(
    router=fake.router,
    prefix="/fake",
    tags=["Fake Generator"],
)
app.include_router(
    router=ef_ir.router,
    prefix="/efir",
    tags=["EF-IR Mock"],
)
app.include_router(
    router=audio.router,
    prefix="/audio",
    tags=["Audio"],
)
app.include_router(
    router=video.router,
    prefix="/video",
    tags=["Video"],
)
# 'catch all' has to be the last router
app.include_router(
    router=catch_all.router,
    tags=["Catch All"],
    dependencies=[Depends(api_user)],
    include_in_schema=False,
)

# websocket
app.add_websocket_route(
    route=echo,
    path="/ws/echo",
)

# middleware
app.add_middleware(CatchAll)
app.add_middleware(HttpLogging)

# exception handlers
# app.add_exception_handler(exc_class_or_status_code=..., handler=...)


@app.on_event("startup")
async def startup():
    create_database_model()


@app.on_event("shutdown")
async def shutdown():
    """shutdown"""
