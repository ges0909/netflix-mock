import logging
from http.client import responses

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class HttpLogging(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        query_params = [f"{name}={value}" for name, value in request.query_params.items()]
        query_string = "?" + "&".join(query_params) if query_params else ""
        logger.debug(
            "%s:%i >> %s %s%s",
            request.client.host,
            request.client.port,
            request.method,
            request.url.path,
            query_string,
        )
        response = await call_next(request)
        logger.debug(
            "%s:%i << %s %s %i (%s)",
            request.client.host,
            request.client.port,
            request.method,
            request.url.path,
            response.status_code,
            responses[response.status_code],
        )
        return response
