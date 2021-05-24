import logging
import re
from pathlib import Path

import fastapi
import pkg_resources
from fastapi import status
from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from httpx import HTTPError
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError

from netflix_mock.routers import users, settings, weather, templates, upload, home
from netflix_mock.schemas.error import Error
from netflix_mock.settings import Settings

logger = logging.getLogger(__name__)

settings_ = Settings()
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


@app.on_event("startup")
async def startup():
    """models connect"""


@app.on_event("shutdown")
async def shutdown():
    """models disconnect"""


@app.middleware("http")
async def unhandled_exceptions(request: Request, call_next) -> Response:
    try:
        response = await call_next(request)
        return response
    except (HTTPError, SQLAlchemyError) as error:
        error_msg = ", ".join(error.args)
    except ValidationError as error:
        msg_parts = re.split(r"\s*\n+\s*", str(error))
        error_msg = ", ".join(msg_parts)
    return Response(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=Error(error=error_msg).json(),
        media_type="application/json",
    )


# @app.middleware("http")
# async def redirect_to_index(request: Request, call_next) -> Response:
#     if request.url.path.startswith("/manual") and not request.url.path.endswith("index.html"):
#         # request._url = request.url.replace(path=request.url.path + "/index.html")
#         parts = request.url.path.split("/")
#         parts = [p for p in parts if p]
#         index_html = Path(__file__).parent.parent / "site" / "/".join(parts[1:]) / "index.html"
#         logger.info(index_html)
#         return FileResponse(str(index_html))
#     return await call_next(request)
