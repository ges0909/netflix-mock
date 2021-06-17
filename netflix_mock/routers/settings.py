from typing import Any, Dict

import fastapi
from fastapi import Body, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from netflix_mock.schemas.error import Error
from netflix_mock.schemas.settings import SettingsOut
from netflix_mock.schemas.success import Success
from netflix_mock.services import settings_service
from netflix_mock.settings import get_settings

router = fastapi.APIRouter()


@router.get(
    path="",
    response_model=SettingsOut,
    responses={
        401: {"model": Error},
        500: {"model": Error},
    },
)
async def read_settings():
    """Read settings."""
    settings = get_settings()
    return SettingsOut.from_orm(settings)


@router.post(
    path="",
    response_model=Success,
    responses={
        401: {"model": Error},
        409: {"model": Error},
        500: {"model": Error},
    },
)
async def update_settings(
    settings: Dict[str, Any] = Body(...),
):
    """Update settings."""
    try:
        updated = settings_service.update_settings(
            settings=get_settings(),
            settings_to_update=settings,
        )
    except ValidationError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        )
    return JSONResponse(
        content=updated,
        status_code=status.HTTP_200_OK,
    )
