from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from pasteshare.core.templates import templates

router = APIRouter(include_in_schema=False)


@router.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("web/index.html", {"request": request})
