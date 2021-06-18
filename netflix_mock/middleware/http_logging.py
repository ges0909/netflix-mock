import logging
from http.client import responses

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class HttpLogging(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        query_params = [f"{k}={v}" for k, v in request.query_params.items()]
        query_params = "?" + "&".join(query_params) if query_params else ""
        logger.info(
            ">> %s:%i %s %s%s",
            request.client.host,
            request.client.port,
            request.method,
            request.url.path,
            query_params,
        )

        headers = [f"{k}={v}" for k, v in request.headers.items()]
        headers = ", ".join(headers)
        logger.debug(">> headers: %s", headers)

        response = await call_next(request)

        logger.info(
            "<< %s:%i %i (%s)",
            request.client.host,
            request.client.port,
            response.status_code,
            responses[response.status_code],
        )

        headers = [f"{k}={v}" for k, v in response.headers.items()]
        headers = ", ".join(headers)
        logger.debug("<< headers %s", headers)

        return response
