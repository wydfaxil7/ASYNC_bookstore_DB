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
if not FRONTEND_DIR.exists():
    FRONTEND_DIR = BASE_DIR.parent / "frontend"
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


@app.get("/ui/books/write", include_in_schema=False)
async def frontend_books_write():
    return _ui_file("books-write.html")


@app.get("/ui/books/view", include_in_schema=False)
async def frontend_books_view():
    return _ui_file("books-view.html")


@app.get("/ui/books/search", include_in_schema=False)
async def frontend_books_search():
    return _ui_file("books-search.html")


@app.get("/ui/books/ai-search", include_in_schema=False)
async def frontend_books_ai_search():
    return _ui_file("books-ai-search.html")


@app.get("/ui/books/ai-summary", include_in_schema=False)
async def frontend_books_ai_summary():
    return _ui_file("books-ai-summary.html")


@app.get("/ui/books/ai-recommendations", include_in_schema=False)
async def frontend_books_ai_recommendations():
    return _ui_file("books-ai-recommendations.html")


@app.get("/ui/profile", include_in_schema=False)
async def frontend_profile():
    return _ui_file("profile.html")

