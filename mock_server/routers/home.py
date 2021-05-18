import fastapi
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

router = fastapi.APIRouter()


@router.get("/", include_in_schema=False)
async def home(request: Request):
    templates = Jinja2Templates("templates")
    return templates.TemplateResponse(name="index.html", context={"request": request})
