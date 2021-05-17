import fastapi
from fastapi.templating import Jinja2Templates
from starlette.requests import Request

templates = Jinja2Templates("templates")

router = fastapi.APIRouter()


@router.get("/", include_in_schema=False)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
