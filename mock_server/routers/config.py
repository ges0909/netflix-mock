import fastapi
from fastapi import Depends

from mock_server.config import settings
from mock_server.deps import get_basic_auth

router = fastapi.APIRouter()


@router.get("/config")
async def read_settings(_: str = Depends(get_basic_auth)):
    """Get app settings."""
    return settings.dict()
