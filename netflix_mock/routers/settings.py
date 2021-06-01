from typing import Any, Dict, List

import fastapi
from fastapi import Body, Depends, HTTPException, status
from pydantic import ValidationError

from netflix_mock.common.responses import (
    HTTP_401_UNAUTHORIZED,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from netflix_mock.common.settings import Settings
from netflix_mock.depends.basic_auth import admin_user
from netflix_mock.schemas.settings import SettingsOut
from netflix_mock.schemas.success import Success

router = fastapi.APIRouter()


def _update_settings(settings: Settings, settings_to_update: Dict[str, Any]) -> List[str]:
    changed_keys = []
    for key, value in settings_to_update.items():
        if key in settings.dict():
            if isinstance(value, dict):
                changed_keys_ = _update_settings(getattr(settings, key), settings_to_update[key])
                changed_keys.extend(changed_keys_)
            elif isinstance(value, list):
                pass
            else:
                setattr(settings, key, value)  # validate_assignment = True
                changed_keys.append(key)
    return changed_keys


@router.get(
    path="",
    response_model=SettingsOut,
    responses={
        **HTTP_401_UNAUTHORIZED,
        **HTTP_500_INTERNAL_SERVER_ERROR,
    },
)
async def read_settings(
    _: None = Depends(admin_user),
):
    """Read settings."""
    return SettingsOut.from_orm(Settings())


@router.post(
    path="",
    response_model=Success,
    responses={
        **HTTP_401_UNAUTHORIZED,
        **HTTP_409_CONFLICT,
        **HTTP_500_INTERNAL_SERVER_ERROR,
    },
)
async def update_settings(
    settings: Dict[str, Any] = Body(...),
    _: None = Depends(admin_user),
):
    """Update settings."""
    try:
        changed_keys = _update_settings(settings=Settings(), settings_to_update=settings)
    except ValidationError as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(error),
        )
    return Success(detail=f"settings changed: {', '.join(changed_keys)}")
