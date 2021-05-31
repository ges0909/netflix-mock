from typing import Any, Dict

import fastapi
from fastapi import Body, Depends

from netflix_mock.depends.basic_auth import admin_user
from netflix_mock.schemas.settings import SettingsOut
from netflix_mock.schemas.success import Success
from netflix_mock.utils.settings import Settings

router = fastapi.APIRouter()


# def _update_settings(settings: Settings, new_settings: Dict[str, Any]):
#     settings_ = settings.dict()
#     for key, value in new_settings.items():
#         if key in settings:
#             if isinstance(value, dict):
#                 _update_settings(settings[key], new_settings[key])
#             elif isinstance(value, list):
#                 pass
#             else:
#                 setattr(settings, key, value)  # validate_assignment = True


@router.get(path="")
async def read_settings(_: bool = Depends(admin_user)):
    """Read settings."""
    return SettingsOut.from_orm(Settings())


@router.post(path="")
async def change_settings(
    settings_in: Dict[str, Any] = Body(...),
    _: bool = Depends(admin_user),
):
    """Update settings."""
    # _update_settings(settings=Settings(), new_settings=settings_in)
    return Success(detail="settings changed")
