import fastapi
from fastapi.responses import RedirectResponse

router = fastapi.APIRouter()


@router.get("/guide")
async def redirect() -> RedirectResponse:
    response = RedirectResponse(url="/guide/index.html")
    return response
