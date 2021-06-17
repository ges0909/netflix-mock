import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class HttpLogging(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        logger.debug(
            "%s:%i >> %s %s",
            request.client.host,
            request.client.port,
            request.method,
            request.url.path,
        )
        response = await call_next(request)
        logger.debug(
            "%s:%i << %s %s %i",
            request.client.host,
            request.client.port,
            request.method,
            request.url.path,
            response.status_code,
        )
        return response
