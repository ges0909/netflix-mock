import fastapi
from starlette.responses import JSONResponse

from netflix_mock.common.responses import (
    HTTP_401_UNAUTHORIZED,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from netflix_mock.services.fake_service import get_fake_response

router = fastapi.APIRouter()


@router.put(
    path="",
    responses={
        **HTTP_401_UNAUTHORIZED,
        **HTTP_500_INTERNAL_SERVER_ERROR,
    },
)
async def fake_put(
    path: str = None,
    status_code: str = "200",
):
    return JSONResponse(
        content=get_fake_response(
            method="put",
            path=path,
            status_code=status_code,
        ),
        status_code=int(status_code),
    )


@router.delete(
    path="",
    responses={
        **HTTP_401_UNAUTHORIZED,
        **HTTP_500_INTERNAL_SERVER_ERROR,
    },
)
async def fake_delete(
    path: str = None,
    status_code: str = "204",
):
    return JSONResponse(
        content=get_fake_response(
            method="delete",
            path=path,
            status_code=status_code,
        ),
        status_code=int(status_code),
    )
