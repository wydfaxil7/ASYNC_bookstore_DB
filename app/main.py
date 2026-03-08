import asyncio
from fastapi import FastAPI
from app.routers import books
from app.database import engine,Base

app = FastAPI()

# #create tables
# @app.on_event("startup")
# async def startup():
#     async with engine.begin() as conn:
#         await conn.run_sync(Base.metadata.create_all)

app.include_router(books.router)

@app.get("/")
async def root():
    return {"message": "Hello World, ope all are okay :)"}