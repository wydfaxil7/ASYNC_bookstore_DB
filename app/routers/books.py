from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app import schemas, models
from app.database import get_db

router = APIRouter()

#CREATE
@router.post("/books", response_model=schemas.BookResponse)
async def create_book(book:schemas.BookCreate, db: AsyncSession = Depends(get_db)):
    db_book = models.Book(name=book.name)
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book

#GET all books
@router.get("/books", response_model=List[schemas.BookResponse])
async def get_books(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Book))
    return result.scalars().all()

#Read one
@router.get("/books/{book_id}", response_model=schemas.BookResponse)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Book).where(models.Book.id == book_id))
    db_book = result.scalar_one_or_none()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

#update
@router.put("/books/{book_id}", response_model=schemas.BookResponse)
async def update_book(book_id: int, book: schemas.BookUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Book).where(models.Book.id == book_id))
    db_book = result.scalar_one_or_none()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    db_book.name = book.name
    await db.commit()
    await db.refresh(db_book)
    return db_book

#DELETE
@router.delete("/books/{book_id}")
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Book).where(models.Book.id == book_id))
    db_book = result.scalar_one_or_none()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    await db.delete(db_book)
    await db.commit()
    return {"message": "Book deleted successfully"}