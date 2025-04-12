from fastapi import APIRouter, Request, Form, Response
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from passlib.hash import bcrypt
from datetime import datetime
from module.database import create_user, get_user_by_email, get_user_by_username

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse)
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/login", response_class=HTMLResponse)
async def login_post(
    request: Request,
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
):
    user = get_user_by_username(username)

    if not user or not bcrypt.verify(password, user["password_hash"]):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "login_error": True},
        )

    request.session["user"] = {
        "id": user["id"],
        "username": user["username"],
        "last_active": datetime.utcnow().timestamp(),
    }

    return templates.TemplateResponse(
        "login.html",
        {"request": request, "login_success": True},
    )


@router.get("/logout", response_class=HTMLResponse)
async def logout(request: Request):
    request.session.clear()
    return templates.TemplateResponse("logout.html", {"request": request})


@router.get("/register", response_class=HTMLResponse)
async def register_get(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register", response_class=HTMLResponse)
async def register_post(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):
    if get_user_by_email(email) or get_user_by_username(username):
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "error": "Email or username already exists."},
        )

    create_user(username, email, bcrypt.hash(password))
    return templates.TemplateResponse(
        "login.html", {"request": request, "success": "Registered successfully"}
    )
