from fastapi import APIRouter, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from module.database import fetch_gadgets
from typing import Annotated

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get(
    "/",
    response_class=HTMLResponse,
    tags=["Pages"],
    summary="Index Page",
    description="Render the public landing page with gadget list hidden.",
)
async def index(request: Request):
    gadgets = fetch_gadgets()
    return templates.TemplateResponse(
        "index.html", {"request": request, "gadgets": gadgets, "show_gadgets": False}
    )


@router.get(
    "/home",
    response_class=HTMLResponse,
    tags=["Pages"],
    summary="User Home",
    description="Render the home page for logged-in users only.",
)
async def home_page(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    return templates.TemplateResponse("home.html", {"request": request, "user": user})


@router.get(
    "/search",
    tags=["Gadget Search"],
    summary="Search Gadgets",
    description="Search for gadgets by name and return matches.",
    response_description="List of gadget names matching the query",
    responses={
        200: {"description": "Search results"},
        422: {"description": "Query too short"},
    },
)
async def search_gadgets(
    q: Annotated[str, Query(..., min_length=1, description="Gadget name or keyword")],
):
    all_gadgets = fetch_gadgets()
    results = [g["name"] for g in all_gadgets if q.lower() in g["name"].lower()]
    return JSONResponse(content=results)


@router.get(
    "/gadgets",
    response_class=HTMLResponse,
    tags=["Gadget Search"],
    summary="Gadgets Page",
    description="Show a full list of gadgets for logged-in users.",
)
async def gadgets_page(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/login", status_code=303)

    gadgets = fetch_gadgets()
    return templates.TemplateResponse(
        "gadgets.html", {"request": request, "user": user, "gadgets": gadgets}
    )
