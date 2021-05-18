import fastapi
from fastapi.requests import Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

router = fastapi.APIRouter()

templates = Jinja2Templates("templates")


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse(name="index.html", context={"request": request})
