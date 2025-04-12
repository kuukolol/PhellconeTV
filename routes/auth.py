from fastapi import APIRouter, Request, Form, Response, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from passlib.hash import bcrypt
from datetime import datetime
from module.database import create_user, get_user_by_email, get_user_by_username

router = APIRouter()
templates = Jinja2Templates(directory="templates")


@router.get("/login", response_class=HTMLResponse, tags=["Authentication"])
async def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post(
    "/login",
    response_class=HTMLResponse,
    tags=["Authentication"],
    responses={
        200: {"description": "Login success or fail. HTML rendered."},
        401: {"description": "Invalid credentials"},
    },
)
async def login_post(
    request: Request,
    response: Response,
    username: str = Form(..., example="techdude99"),
    password: str = Form(..., example="strongPassword123"),
):
    user = get_user_by_username(username)

    if not user or not bcrypt.verify(password, user["password_hash"]):
        response.status_code = status.HTTP_401_UNAUTHORIZED
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


@router.get("/logout", response_class=HTMLResponse, tags=["Authentication"])
async def logout(request: Request):
    request.session.clear()
    return templates.TemplateResponse("logout.html", {"request": request})


@router.get("/register", response_class=HTMLResponse, tags=["Authentication"])
async def register_get(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post(
    "/register",
    response_class=HTMLResponse,
    tags=["Authentication"],
    responses={
        200: {"description": "Registration success or fail. HTML rendered."},
        400: {"description": "User/email already exists"},
    },
)
async def register_post(
    request: Request,
    response: Response,
    username: str = Form(..., example="newuser"),
    email: str = Form(..., example="newuser@example.com"),
    password: str = Form(..., example="securePassword123"),
):
    if get_user_by_email(email) or get_user_by_username(username):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return templates.TemplateResponse(
            "register.html",
            {"request": request, "register_error": True},
        )

    create_user(username, email, bcrypt.hash(password))
    return templates.TemplateResponse(
        "register.html", {"request": request, "register_success": True}
    )
