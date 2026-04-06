#app/services/books.py
from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.Repository import books as repo
from typing import List
from app.models import Book
from app.utils.wrappers import serv_wrapper
from app.schemas import BookListResponse, BookResponse
from datetime import date, datetime
import re

from app.services import ai as ai_service

def parse_partial_date(date_str: str) -> tuple[date, date]:
    """
    Parse partial date strings into start and end date range.
    Supports: YYYY, YYYY-MM, YYYY-MM-DD
    """
    if not date_str:
        return None, None
    
    # Validate format
    if not re.match(r'^\d{4}(-\d{2})?(-\d{2})?$', date_str):
        raise HTTPException(
            status_code=400, 
            detail="Date must be in format YYYY, YYYY-MM, or YYYY-MM-DD"
        )
    
    parts = date_str.split('-')
    
    if len(parts) == 1:  # YYYY
        year = int(parts[0])
        start = date(year, 1, 1)
        end = date(year, 12, 31)
    elif len(parts) == 2:  # YYYY-MM
        year, month = int(parts[0]), int(parts[1])
        start = date(year, month, 1)
        # Get last day of month
        if month == 12:
            end = date(year, 12, 31)
        else:
            end = date(year, month + 1, 1) - date.resolution
    else:  # YYYY-MM-DD
        year, month, day = int(parts[0]), int(parts[1]), int(parts[2])
        start = end = date(year, month, day)
    
    return start, end

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
                            end_date,
                            sort_by: str | None,
                            order: str | None
                            ):
    
    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit exceeds(max 100)")
    
    # Validate sorting parameters
    allowed_sort_fields = {"name", "author", "published_date", "genre"}
    allowed_orders = {"asc", "desc"}
    
    if sort_by and sort_by not in allowed_sort_fields:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid sort_by field. Allowed: {', '.join(allowed_sort_fields)}"
        )
    
    if order and order not in allowed_orders:
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid order. Allowed: {', '.join(allowed_orders)}"
        )
    
    # Set defaults if not provided
    if not sort_by:
        sort_by = "published_date"
    if not order:
        order = "desc"
    
    # Parse partial dates
    actual_start_date = None
    actual_end_date = None
    
    if start_date:
        actual_start_date, _ = parse_partial_date(start_date)
    
    if end_date:
        _, actual_end_date = parse_partial_date(end_date)
    
    books, total = await repo.get_books_with_filters(db, limit, offset, author, genre, actual_start_date, actual_end_date, sort_by, order)
    
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
                              ) -> BookListResponse:
    """
    Handles searching books with filter and pagination
    """

    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit too large (max 100)")

    books, total = await repo.search_book(db, q, genre, limit, offset)
    books_data = [BookResponse.model_validate(book) for book in books]

    return BookListResponse(
        total=total,
        limit=limit,
        offset=offset,
        data=books_data,
        message="No Data found" if not books_data else "Search results fetched successfully",
    )

@serv_wrapper
async def get_book_summary_service(db: AsyncSession, book_id: int) -> dict:
    """
    Generate a story-like summary for a book using AI.
    
    Args:
        db: Database session
        book_id: ID of the book to summarize
    
    Returns:
        Dict with book_id and generated summary
    """
    # Fetch the book
    book = await repo.get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # Check if book has a description
    if not book.description:
        raise HTTPException(status_code=400, detail="Book has no description to summarize")
    
    # Create AI prompt with book details
    prompt = f"""You are a creative storyteller. Based on the following book details, write an engaging, story-like summary that captures the essence of the book in 2-3 paragraphs. Make it vivid and captivating, as if you're telling the story to a friend.

Book Title: {book.name}
Author: {book.author}
Genre: {book.genre or 'Not specified'}
Publication Date: {book.published_date or 'Not specified'}
Description: {book.description}

Write a compelling summary that makes someone want to read the book. Focus on the key themes, characters, and emotional journey. Keep it engaging and spoiler-free."""

    try:
        # Generate summary using AI
        summary = await ai_service.generate_summary(prompt)
        
        return {
            "book_id": book.id,
            "name": book.name,
            "author": book.author,
            "summary": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate summary: {str(e)}")

@serv_wrapper
async def get_book_summary_by_name_service(db: AsyncSession, name: str):
    """
    Generate AI summary for a book by name (case-insensitive search).
    Returns the first match if multiple books have the same name.
    """
    # Find book by name (case-insensitive)
    result = await db.execute(
        select(Book).where(Book.name.ilike(f"%{name}%")).limit(1)
    )
    book = result.scalar_one_or_none()
    
    if not book:
        raise HTTPException(status_code=404, detail=f"Book with name containing '{name}' not found")
    
    if not book.description:
        raise HTTPException(status_code=400, detail="Book has no description to summarize")
    
    # Create AI prompt with book details
    prompt = f"""You are a creative storyteller. Based on the following book details, write an engaging, story-like summary that captures the essence of the book in 2-3 paragraphs. Make it vivid and captivating, as if you're telling the story to a friend.

Book Title: {book.name}
Author: {book.author}
Genre: {book.genre or 'Not specified'}
Publication Date: {book.published_date or 'Not specified'}
Description: {book.description}

Write a compelling summary that makes someone want to read the book. Focus on the key themes, characters, and emotional journey. Keep it engaging and spoiler-free."""

    try:
        # Generate summary using AI
        summary = await ai_service.generate_summary(prompt)
        
        return {
            "book_id": book.id,
            "name": book.name,
            "author": book.author,
            "summary": summary
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate summary: {str(e)}")

@serv_wrapper
async def ai_search_book_service(db: AsyncSession, query: str, limit: str, offset:str):
    """
    Handles searching books with GROQ API
    """
    if limit > 100:
        raise HTTPException(status_code=400, detail="Limit too large")
    
    books, total = await ai_service.ai_search_service(db, query, limit, offset)

    books_data = [BookResponse.model_validate(book) for book in books]

    return BookListResponse(
        total = total, 
        limit = limit,
        offset = offset,
        data = books_data,
        message = "No Data found" if not books_data else "AI search successful"
    )

