#main.py
from fastapi import FastAPI
from app.routers import books, auth
from app.database import engine, Base

app = FastAPI()
app.include_router(auth.router)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Tables are ready")

app.include_router(books.router)

@app.get("/")
async def root():
    return {"message": "Hello World, hope all are okay :)"}

