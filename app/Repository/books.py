#app/Repository/books.py
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Book
from sqlalchemy import or_, func, and_
from datetime import date

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

async def create_bulk_books(db: AsyncSession, books_date: List[dict]):
    """
    Inserts books in bulk
    """
    db_books = [Book(**book) for book in books_date]

    db.add_all(db_books)
    await db.commit()
    
    for book in db_books:
        await db.refresh(book)

    return db_books
    

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

async def search_book(db: AsyncSession,
                      q: str | None = None,
                      genre: str | None = None,
                      limit: int = 10,
                      offset: int = 0,
                      ) -> List[Book]:
    """
    Search book by title and author, with optional genre filter and pagination
    """

    query = select(Book)

    # Search by title OR author
    if q:
        search_term = f"%{q}%"
        query = query.where(
            or_(
                Book.name.ilike(search_term),
                Book.author.ilike(search_term)
            )
        )

    # Filter by Genre
    if genre:
        query = query.where(Book.genre == genre)
        
    #Pagination
    query = query.offset(offset).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()

# async def get_books_with_count(db: AsyncSession,
#                                limit: int = 10,
#                                offset: int = 0
#                                ):
#     """
#     Fetch books with total count for pagination
#     """
#     #Total count
#     total_result = await db.execute(
#         select(func.count()).select_from(Book)
#     )
#     total = total_result.scalar()

#     #Paginated Data
#     result = await db.execute(
#         select(Book).offset(offset).limit(limit)
#     )
#     books = result.scalars().all()
#     return books, total

async def get_books_with_filters(db: AsyncSession,
                                 limit: int,
                                 offset: int,
                                 author: str | None = None,
                                 genre: str | None = None,
                                 start_date: date | None = None,
                                 end_date: date | None = None):
    """
    Fetch books with dynamic filters and total count
    """

    query = select(Book)
    count_query = select(func.count()).select_from(Book)

    filters = []

    # Author filter (case-insensitive match)
    if author:
        filters.append(Book.author.ilike(f"%{author}%"))

    # Genre filter
    if genre: 
        filters.append(Book.genre == genre)

    # Start-Date filter
    if start_date:
        filters.append(Book.published_date >= start_date)

    # End-Date filters
    if end_date:
        filters.append(Book.published_date <= end_date)

    # This will apply filter if any exists
    if filters:
        query = query.where(and_(*filters))
        count_query = count_query.where(and_(*filters))

    # Total count
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Pagination
    query = query.limit(limit).offset(offset)
    result = await db.execute(query)

    books = result.scalars().all()

    return books, total