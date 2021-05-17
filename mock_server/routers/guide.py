import fastapi
from fastapi.responses import RedirectResponse

router = fastapi.APIRouter()


@router.get("", include_in_schema=False)
async def redirect() -> RedirectResponse:
    response = RedirectResponse(url="/guide/index.html")
    return response
