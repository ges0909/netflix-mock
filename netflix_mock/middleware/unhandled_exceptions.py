import logging

from fastapi import status
from fastapi.requests import Request
from fastapi.responses import Response
from httpx import HTTPError
from sqlalchemy.exc import SQLAlchemyError

from netflix_mock.app import app
from netflix_mock.schemas.error import Error

logger = logging.getLogger(__name__)


@app.middleware("http")
async def unhandled_exceptions(request: Request, call_next) -> Response:
    try:
        response = await call_next(request)
        return response
    except (HTTPError, SQLAlchemyError) as error:
        detail = ", ".join(error.args)
        return Response(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=Error(detail=detail).json(),
            media_type="application/json",
        )
