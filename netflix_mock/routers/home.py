from pathlib import Path

import fastapi
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

router = fastapi.APIRouter()


templates_dir = Path(__file__).parent / ".." / "templates"

templates = Jinja2Templates(directory=str(templates_dir))


@router.get("/", response_class=HTMLResponse, include_in_schema=False)
async def home(request: Request):
    return templates.TemplateResponse(
        name="index.html",
        context={"request": request},
    )
