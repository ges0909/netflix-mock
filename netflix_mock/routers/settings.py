from typing import Any, Dict

import fastapi
from fastapi import Body, Depends, HTTPException, status
from pydantic import ValidationError

from netflix_mock.common.settings import Settings
from netflix_mock.depends.basic_auth import admin_user
from netflix_mock.schemas.settings import SettingsOut
from netflix_mock.schemas.success import Success

router = fastapi.APIRouter()


def _update_settings(settings: Settings, settings_to_update: Dict[str, Any]):
    for key, value in settings_to_update.items():
        if key in settings.dict():
            if isinstance(value, dict):
                _update_settings(getattr(settings, key), settings_to_update[key])
            elif isinstance(value, list):
                pass
            else:
                setattr(settings, key, value)  # validate_assignment = True


@router.get(path="")
async def read_settings(_: bool = Depends(admin_user)):
    """Read settings."""
    return SettingsOut.from_orm(Settings())


@router.post(path="")
async def change_settings(
    settings: Dict[str, Any] = Body(...),
    _: bool = Depends(admin_user),
):
    """Update settings."""
    try:
        _update_settings(settings=Settings(), settings_to_update=settings)
    except ValidationError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        )
    return Success(detail="settings changed")
