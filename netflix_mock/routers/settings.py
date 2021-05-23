from typing import Dict, Any

import fastapi
from fastapi import Depends, Body

from netflix_mock.basic_auth import admin_user
from netflix_mock.schemas.settings import SettingsOut
from netflix_mock.schemas.success import Success
from netflix_mock.settings import get_settings

router = fastapi.APIRouter()


@router.get("/")
async def read_settings(_: bool = Depends(admin_user)):
    """Read application settings."""
    settings = get_settings()
    return SettingsOut.from_orm(settings)


@router.post("/")
async def change_settings(
    settings_: Dict[str, Any] = Body(...),
    _: bool = Depends(admin_user),
):
    """Change application settings."""
    settings = get_settings()
    for key, value in settings_.items():
        setattr(settings, key, value)  # validate_assignment = True
    return Success(detail=f"{', '.join(settings_.keys())} changed sucessfully")
