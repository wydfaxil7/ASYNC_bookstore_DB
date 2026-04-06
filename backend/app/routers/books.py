#app/routers/books.py
from fastapi import APIRouter, Depends, Query, Security
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app import schemas
from datetime import date
from app.database import get_db
from app.services import books as services
from app.services.ai import ai_search_service, ai_recommend_book_service
from app.services.ai_prompts import build_search_prompt
from app.schemas import BookListResponse, AuthorResponse, BookSummaryResponse
from app.dependencies.auth_dependencies import require_admin, get_current_user
from fastapi import HTTPException, status
from app.dependencies.security import bearer_scheme, get_current_user_from_token


router = APIRouter()

@router.post("/books", response_model=schemas.BookResponse)
async def create_book(
    book: schemas.BookCreate, 
    db: AsyncSession = Depends(get_db),
    admin: dict = Security(require_admin)
):
    """
    Creates a new book
    """
    return await services.create_book_service(db, book.model_dump())

@router.post("/books/bulk", response_model=List[schemas.BookResponse])
async def create_bulk_books(
    payload :schemas.BookBulkCreate,
    db: AsyncSession = Depends(get_db),
    admin: dict = Security(require_admin)
):
    """
    Create books in bulk
    """
    return await services.create_bulk_books_service(db, [book.model_dump() for book in payload.books])

@router.get("/books", response_model=schemas.BookListResponse)
async def get_books(
    limit: int = 10,
    offset: int = 0,
    author: str | None = None,
    genre: str | None = None,
    start_date: str | None = None,
    end_date: str | None = None,
    sort_by: str | None = None,
    order: str | None = None,
    db: AsyncSession = Depends(get_db)
):
    """
    Fetche all books
    """
    return await services.get_books_service(db, limit, offset, author, genre, start_date, end_date, sort_by, order)

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

@router.get("/books/ai-search", response_model=schemas.AISearchResponse)
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

    # Convert ORM → Pydantic if books exist
    if result.get("data"):
        result["data"] = [
            schemas.BookResponse.model_validate(book)
            for book in result["data"]
        ]
    
    return result

@router.get("/books/recommendations", response_model=schemas.BookListResponse)
async def ai_recommend_books(
    title: str,
    limit: int = 5,
    offset: int = 0,
    db: AsyncSession = Depends(get_db)
):
    """
    Get AI-based recommendations fom the DB
    """
    result = await ai_recommend_book_service(db, title, limit, offset)
    books_data = [schemas.BookResponse.model_validate(book) for book in result["data"]]
    return schemas.BookListResponse(
        total = result["total"],
        limit = result["limit"],
        offset = result["offset"],
        data = books_data,
        message = result["message"]
    )

@router.get("/books/{book_id}", response_model=schemas.BookResponse)
async def get_book(book_id: int, db: AsyncSession = Depends(get_db)):
    """
    Fetch a book by its ID
    """
    return await services.get_book_service(db, book_id)

@router.put("/books/{book_id}", response_model=schemas.BookResponse)
async def update_book(
    book_id: int, 
    book: schemas.BookUpdate, 
    db: AsyncSession = Depends(get_db),
    admin: dict = Security(require_admin)
):
    """
    Updates an existing book
    """
    return await services.update_book_service(db, book_id, book.model_dump())

@router.delete("/books/{book_id}")
async def delete_book(
    book_id: int, 
    db: AsyncSession = Depends(get_db),
    admin: dict = Security(require_admin)
):
    """
    Delete a book by its ID
    """
    return await services.delete_book_service(db, book_id)

# @router.get("/books/{book_id}/summary", response_model=BookSummaryResponse)
# async def get_book_summary(
#     book_id: int,
#     db: AsyncSession = Depends(get_db)
# ):
#     """
#     Generate a story-like summary of a book using AI.
#
#     Uses the book's description and metadata to create an engaging summary.
#     """
#     return await services.get_book_summary_service(db, book_id)


@router.get("/books/summary/search", response_model=BookSummaryResponse)
async def get_book_summary(
    id: int = Query(None, description="Book ID to get summary for"),
    name: str = Query(None, description="Book name to search for (partial matching supported)"),
    db: AsyncSession = Depends(get_db)
):
    """
    Generate a story-like summary of a book using AI.
    
    Can search by either book ID or book name. If both are provided, ID takes precedence.
    Uses the book's description and metadata to create an engaging summary.
    """
    if id is not None:
        return await services.get_book_summary_service(db, id)
    elif name is not None:
        return await services.get_book_summary_by_name_service(db, name)
    else:
        raise HTTPException(status_code=400, detail="Either 'id' or 'name' parameter must be provided")

# @router.delete("/books/{book_id}")
# async def admin_delete_book(
#     id: int,
#     admin = Depends(require_admin)
# ):
#     """
#     Admin-only endpoint to delete a book by ID.
#     """
#     return {"message": f"Admin user '{admin.username}' deleted book with ID {id}"}


# """TESTING WRAPPERS"""
# @router.get("/test-error")
# async def test_error(db: AsyncSession = Depends(get_db)):
#     from app.services import books as services
    
#     # This will fail because 'non_existent_book_id' is negative and will not be found
#     return await services.get_book_service(db, book_id=-1)

