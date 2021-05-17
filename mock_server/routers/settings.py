import fastapi
from fastapi import Depends

from mock_server.depends.app_settings import app_settings
from mock_server.depends.basic_auth import basic_auth
from mock_server.settings import Settings

router = fastapi.APIRouter()


@router.get("/")
async def read_settings(
    _: str = Depends(basic_auth),
    settings: Settings = Depends(app_settings),
):
    """Get app settings."""
    return settings.dict()
