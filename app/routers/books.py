#app/routers/books.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app import schemas
from datetime import date
from app.database import get_db
from app.services import books as services
from app.services.ai import ai_search_service
from app.services.ai_prompts import build_search_prompt
from app.schemas import BookListResponse, AuthorResponse

router = APIRouter()

@router.post("/books", response_model=schemas.BookResponse)
async def create_book(book: schemas.BookCreate, db: AsyncSession = Depends(get_db)):
    """
    Creates a new book
    """
    return await services.create_book_service(db, book.model_dump())

@router.post("/books/bulk", response_model=List[schemas.BookResponse])
async def create_bulk_books(payload :schemas.BookBulkCreate,
                            db: AsyncSession = Depends(get_db)):
    """
    Create books in bulk
    """
    return await services.create_bulk_books_service(db, [book.model_dump() for book in payload.books])

@router.get("/books", response_model=schemas.BookListResponse)
async def get_books(limit: int = 10,
                    offset: int = 0,
                    author: str | None = None,
                    genre: str | None = None,
                    start_date: date | None = None,
                    end_date: date | None= None,
                    db: AsyncSession = Depends(get_db)):
    """
    Fetche all books
    """
    return await services.get_books_service(db, limit, offset, author, genre, start_date, end_date)

@router.get("/books/search", response_model = List[schemas.BookResponse])
async def search_book(
    q: str | None = None,
    genre: str | None = None,
    limit: int = 10,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """
    Search book by title/author and filter by genre
    """
    return await services.search_book_service(db, q, genre, limit, offset)

@router.get("/books/ai-search", response_model=schemas.BookListResponse)
async def ai_search_books(
    query: str,
    limit: int = 10,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """
    Natural Language Search using AI
    """
    result = await ai_search_service(db, query, limit, offset)

    # If result is dict → it's an author-only response
    if isinstance(result, dict):
        return result  # {"author": "Mark Manson"}

    # Otherwise, it's list of books
    books, total = result
    books_data = [schemas.BookResponse.model_validate(book) for book in books]

    return schemas.BookListResponse(
        total=total,
        limit=limit,
        offset=offset,
        data=books_data,
        message="Books fetched successfully" if books_data else "No data found"
    )

@router.get("/books/{book_id}", response_model=schemas.BookResponse)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    """
    Fetch a book by its ID
    """
    return await services.get_book_service(db, book_id)

@router.put("/books/{book_id}", response_model=schemas.BookResponse)
async def update_book(book_id: int, book: schemas.BookUpdate, db: AsyncSession = Depends(get_db)):
    """
    Updates an existing book
    """
    return await services.update_book_service(db, book_id, book.model_dump())

@router.delete("/books/{book_id}")
async def delete_book(book_id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a book by its ID
    """
    return await services.delete_book_service(db, book_id)



# """TESTING WRAPPERS"""
# @router.get("/test-error")
# async def test_error(db: AsyncSession = Depends(get_db)):
#     from app.services import books as services
    
#     # This will fail because 'non_existent_book_id' is negative and will not be found
#     return await services.get_book_service(db, book_id=-1)

