from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from module.database import fetch_gadgets

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/", response_class=HTMLResponse)
async def index(request: Request):
    gadgets = fetch_gadgets()
    return templates.TemplateResponse(
        "index.html", {"request": request, "gadgets": gadgets, "show_gadgets": False}
    )


@router.get("/home", response_class=HTMLResponse)
async def home_page(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse("home.html", {"request": request, "user": user})


@router.get("/search")
async def search_gadgets(q: str = Query(..., min_length=1)):
    all_gadgets = fetch_gadgets()
    results = [g["name"] for g in all_gadgets if q.lower() in g["name"].lower()]
    return JSONResponse(content=results)


@router.get("/gadgets", response_class=HTMLResponse)
async def gadgets_page(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    gadgets = fetch_gadgets()
    return templates.TemplateResponse(
        "gadgets.html", {"request": request, "user": user, "gadgets": gadgets}
    )
