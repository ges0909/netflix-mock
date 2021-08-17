import fastapi

from netflix_mock.schemas.success import Success

router = fastapi.APIRouter()


@router.get(path="{data:path}")
async def get(
    data: str,
) -> Success:
    return Success(detail=data)
