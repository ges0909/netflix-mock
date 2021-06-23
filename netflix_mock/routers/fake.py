import fastapi
from starlette.responses import JSONResponse

from netflix_mock.schemas.api_error import ApiError
from netflix_mock.services import fake_service

router = fastapi.APIRouter()


@router.put(
    path="",
    responses={
        401: {"model": ApiError},
        500: {"model": ApiError},
    },
)
async def fake_put(
    path: str = None,
    status_code: str = "200",
):
    response = fake_service.generate_response(
        method="put",
        path=path,
        status_code=status_code,
    )
    return JSONResponse(
        content=response,
        status_code=int(status_code),
    )


@router.delete(
    path="",
    responses={
        401: {"model": ApiError},
        500: {"model": ApiError},
    },
)
async def fake_delete(
    path: str = None,
    status_code: str = "204",
):
    response = fake_service.generate_response(
        method="delete",
        path=path,
        status_code=status_code,
    )
    return JSONResponse(
        content=response,
        status_code=int(status_code),
    )
