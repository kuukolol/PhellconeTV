from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from datetime import datetime

from module.tags_metadata import tags_metadata
from routes import gadgets, auth

app = FastAPI(
    title="Phelcone Gadget Store",
    version="0.1.0",
    description="A WEBSYS project",
    openapi_tags=tags_metadata,
)


@app.middleware("http")
async def session_timeout_middleware(request: Request, call_next):
    session = request.session
    user = session.get("user")

    if user:
        last_active = session.get("last_active")
        now = datetime.utcnow().timestamp()
        if last_active and now - last_active > 10800:
            request.session.clear()
        else:
            session["last_active"] = now

    response = await call_next(request)
    return response


app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(gadgets.router)
app.include_router(auth.router)
app.add_middleware(SessionMiddleware, secret_key="9@S~`#+WS£74^rKaCp-6H51s[%")