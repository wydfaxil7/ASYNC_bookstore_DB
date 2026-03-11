#app/Repository/books.py
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Book

from typing import List

async def create_book(db: AsyncSession, book_data: dict) -> Book:
    """
    Insert a new book into the database.
    """
    db_book = Book(**book_data)
    db.add(db_book)
    await db.commit()
    await db.refresh(db_book)
    return db_book

async def get_books(db: AsyncSession) -> List[Book]:
    """
    GET all books from the [bookstore] database.
    """
    result = await db.execute(select(Book))
    return result.scalars().all()

async def get_book(db: AsyncSession, book_id: int) -> Book | None:
    """
    Get a book by its [id] from the [bookstore] database.
    """
    result = await db.execute(select(Book).where(Book.id == book_id))
    return result.scalar_one_or_none()

async def update_book(db: AsyncSession, db_book: Book, updates: dict) -> Book:
    """
    Updates an existing book in the [bookstore] database.
    """
    for key, value in updates.items():
        setattr(db_book, key, value)
    await db.commit()
    await db.refresh(db_book)
    return db_book

async def delete_book(db: AsyncSession, db_book: Book) -> None:
    """
    Deletes a book from the [bookstore] database.
    """
    await db.delete(db_book)
    await db.commit()