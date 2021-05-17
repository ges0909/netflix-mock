import fastapi
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

router = fastapi.APIRouter()


@router.get("/", include_in_schema=False)
async def home(request: Request):
    from main import app_root

    templates = Jinja2Templates(directory=app_root / "templates")
    return templates.TemplateResponse(
        name="index.html",
        context={"request": request},
    )
