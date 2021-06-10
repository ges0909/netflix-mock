from typing import Any, Dict

import fastapi
from fastapi import Body, Depends, HTTPException, status
from pydantic import ValidationError

from netflix_mock.depends.basic_auth import admin_user
from netflix_mock.schemas.error import Error
from netflix_mock.schemas.settings import SettingsOut
from netflix_mock.schemas.success import Success
from netflix_mock.services import settings_service
from netflix_mock.settings import Settings

router = fastapi.APIRouter()


@router.get(
    path="",
    response_model=SettingsOut,
    responses={
        401: {"model": Error},
        500: {"model": Error},
    },
    dependencies=[Depends(admin_user)],
)
async def read_settings():
    """Read settings."""
    return SettingsOut.from_orm(Settings())


@router.post(
    path="",
    response_model=Success,
    responses={
        401: {"model": Error},
        409: {"model": Error},
        500: {"model": Error},
    },
    dependencies=[Depends(admin_user)],
)
async def update_settings(
    settings: Dict[str, Any] = Body(...),
):
    """Update settings."""
    try:
        changed_keys = settings_service.update_settings(
            settings=Settings(),
            settings_to_update=settings,
        )
    except ValidationError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        )
    return Success(detail=f"settings changed: {', '.join(changed_keys)}")
