from typing import Dict, Any

import fastapi
from fastapi import Depends, Body

from netflix_mock.basic_auth import admin_user
from netflix_mock.config import Config
from netflix_mock.schemas.settings import SettingsOut
from netflix_mock.schemas.success import Success

router = fastapi.APIRouter()


@router.get("/")
async def read_settings(_: bool = Depends(admin_user)):
    """Read application settings."""
    config = Config()
    return SettingsOut.from_orm(config)


@router.post("/")
async def change_settings(
    settings: Dict[str, Any] = Body(...),
    _: bool = Depends(admin_user),
):
    """Change application settings."""
    config = Config()
    for key, value in settings.items():
        setattr(config, key, value)  # validate_assignment = True
    return Success(detail=f"{', '.join(settings.keys())} changed sucessfully")
