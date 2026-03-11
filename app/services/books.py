#app/services/books.py
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.Repository import books as repo
from typing import List
from app.models import Book
from app.utils.wrappers import serv_wrapper

@serv_wrapper
async def create_book_service(db: AsyncSession, book_data: dict) -> Book:
    """
    Handles creating a new book.
    """
    return await repo.create_book(db, book_data)

@serv_wrapper
async def get_books_service(db: AsyncSession) -> List[Book]:
    """
    Handles fetching/getting all books from the [bookstore] database
    """
    return await repo.get_books(db)

@serv_wrapper
async def get_book_service(db: AsyncSession, book_id: int) -> Book:
    """
    Handles fetching/getting a book by id
    """
    book = await repo.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@serv_wrapper
async def update_book_service(db: AsyncSession, book_id: int, updates: dict) -> Book:
    """
    Handles updating a book by ID
    """
    book = await repo.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return await repo.update_book(db, book, updates)

@serv_wrapper
async def delete_book_service(db: AsyncSession, book_id: int) -> dict:
    """
    Handles deleting a book by ID
    """
    book = await repo.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    await repo.delete_book(db, book)
    return {"message": "Book deleted successfully"}

