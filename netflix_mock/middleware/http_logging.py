import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class HttpLogging(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        logger.debug("> %s %s", request.method, request.url.path)
        response = await call_next(request)
        logger.debug("< %s %s %i", request.method, request.url.path, response.status_code)
        return response
