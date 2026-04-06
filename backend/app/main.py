#main.py
from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from app.routers import books, auth
from app.database import engine, Base

app = FastAPI()
app.include_router(auth.router)

BASE_DIR = Path(__file__).resolve().parent
FRONTEND_DIR = BASE_DIR.parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")
UI_PAGES_DIR = FRONTEND_DIR / "ui" / "pages"


def _ui_file(filename: str) -> FileResponse:
    return FileResponse(UI_PAGES_DIR / filename)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables are ready")

app.include_router(books.router)

@app.get("/")
async def root():
    return {"message": "Hello World, hope all are okay :)"}


@app.get("/ui", include_in_schema=False)
async def frontend_ui():
    return _ui_file("landing.html")


@app.get("/ui/login", include_in_schema=False)
async def frontend_login():
    return _ui_file("login.html")


@app.get("/ui/register", include_in_schema=False)
async def frontend_register():
    return _ui_file("register.html")


@app.get("/ui/dashboard", include_in_schema=False)
async def frontend_dashboard():
    return _ui_file("dashboard.html")


@app.get("/ui/profile", include_in_schema=False)
async def frontend_profile():
    return _ui_file("profile.html")

