import fastapi
from fastapi import Depends

from netflix_mock.auth import get_basic_auth
from netflix_mock.config import get_settings

router = fastapi.APIRouter()


@router.get("/")
async def read_settings(_: str = Depends(get_basic_auth)):
    """Get app settings."""
    settings = get_settings()
    return settings.dict()
