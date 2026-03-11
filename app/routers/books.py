#app/routers/books.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app import schemas
from app.database import get_db
from app.services import books as services

router = APIRouter()

@router.post("/books", response_model=schemas.BookResponse)
async def create_book(book: schemas.BookCreate, db: AsyncSession = Depends(get_db)):
    """
    Creates a new book
    """
    return await services.create_book_service(db, book.dict())

@router.get("/books", response_model=List[schemas.BookResponse])
async def get_books(db: AsyncSession = Depends(get_db)):
    """
    Fetche all books
    """
    return await services.get_books_service(db)

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
    return await services.update_book_service(db, book_id, book.dict())

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