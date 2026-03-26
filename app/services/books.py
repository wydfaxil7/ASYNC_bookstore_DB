#app/services/books.py
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.Repository import books as repo
from typing import List
from app.models import Book
from app.utils.wrappers import serv_wrapper
from app.schemas import BookListResponse, BookResponse

@serv_wrapper
async def create_book_service(db: AsyncSession, book_data: dict) -> Book:
    """
    Handles creating a new book.
    """
    return await repo.create_book(db, book_data)

@serv_wrapper
async def create_bulk_books_service(db: AsyncSession, books: List[dict]):
    """
    Handles creating books in bulk
    """
    db_books = await repo.create_bulk_books(db, books)

    return [BookResponse.model_validate(book) for book in db_books]

@serv_wrapper
async def get_books_service(db: AsyncSession, 
                            limit: int, 
                            offset: int,
                            author: str | None,
                            genre: str | None,
                            start_date,
                            end_date
                            ):
    
    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit exceeds(max 100)")
    
    books, total = await repo.get_books_with_filters(db, limit, offset, author, genre, start_date, end_date)
    
    # Convert ORM objects to Pydantic models
    books_data = [BookResponse.model_validate(book) for book in books]

    # Return Pydantic model instance instead of plain dict
    return BookListResponse(
        total=total,
        limit=limit,
        offset=offset,
        data=books_data,
        message="No Data found" if not books_data else "Books fetched successfully"
    )

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

@serv_wrapper
async def search_book_service(db: AsyncSession,
                              q: str | None,
                              genre: str | None,
                              limit : int,
                              offset: int
                              ) -> List[Book]:
    """
    Handles searching books with filter and pagination
    """

    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit too large (max 100)")

    return await repo.search_book(db, q, genre, limit, offset)
