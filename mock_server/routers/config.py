import fastapi
from fastapi import Depends

from mock_server.config import Settings
from mock_server.deps import get_basic_auth, get_settings

router = fastapi.APIRouter()


@router.get("/config")
async def read_settings(
    _: str = Depends(get_basic_auth),
    settings: Settings = Depends(get_settings),
):
    """Get app settings."""
    return settings.dict()
