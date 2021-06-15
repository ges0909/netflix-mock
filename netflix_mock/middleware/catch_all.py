import logging

from fastapi import status
from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response
from sqlalchemy.exc import SQLAlchemyError
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class CatchAll(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            response = await call_next(request)
            return response
        except SQLAlchemyError as error:
            detail = ", ".join(error.args)
        except Exception as error:
            detail = str(error)
        logger.error("%s", detail)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=dict(detail=detail),
        )
