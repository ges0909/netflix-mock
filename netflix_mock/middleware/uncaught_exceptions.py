import logging
import re

from fastapi import status
from fastapi.requests import Request
from fastapi.responses import Response
from httpx import HTTPError
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.base import BaseHTTPMiddleware

from netflix_mock.schemas.error import Error

logger = logging.getLogger(__name__)


class UncaughtExceptions(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            response = await call_next(request)
            return response
        except (HTTPError, SQLAlchemyError) as error:
            logger.error(error)
            error_msg = ", ".join(error.args)
        except ValidationError as error:
            logger.error(error)
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
