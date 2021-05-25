import fastapi
from fastapi.responses import RedirectResponse

router = fastapi.APIRouter()


@router.get(path="/", include_in_schema=False)
async def redirect_to_manual() -> RedirectResponse:
    return RedirectResponse(url="/manual/home.html")
