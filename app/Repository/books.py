#app/Repository/books.py
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Book
from sqlalchemy import or_, func, and_, asc, desc
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
                                 end_date: date | None = None,
                                 sort_by: str = "published_date",
                                 order: str = "desc"):
    """
    Fetch books with dynamic filters, sorting and total count
    """

    query = select(Book)
    count_query = select(func.count()).select_from(Book)

    filters = []

    # Author filter (case-insensitive match)
    if author:
        filters.append(Book.author.ilike(f"%{author}%"))

    # Genre filter
    if genre: 
        filters.append(Book.genre.ilike(f"%{genre}%"))

    # Start-Date filter
    if start_date:
        filters.append(Book.published_date >= start_date)

    # End-Date filters
    if end_date:
        filters.append(Book.published_date <= end_date)

    # Apply filters if any exist
    if filters:
        query = query.where(and_(*filters))
        count_query = count_query.where(and_(*filters))

    # Apply sorting
    column_map = {
        "name": Book.name,
        "author": Book.author,
        "published_date": Book.published_date,
        "genre": Book.genre
    }
    
    sort_column = column_map.get(sort_by, Book.published_date)
    if order == "desc":
        query = query.order_by(desc(sort_column))
    else:
        query = query.order_by(asc(sort_column))

    # Total count
    total_result = await db.execute(count_query)
    total = total_result.scalar()

    # Pagination
    query = query.limit(limit).offset(offset)
    result = await db.execute(query)

    books = result.scalars().all()

    return books, total


async def search_books_by_keywords(
    db: AsyncSession,
    keywords: list[str],
    limit: int = 10,
    offset: int = 0,
    author: str | None = None,
    genre: str | None = None
) -> tuple[list[Book], int]:
    """
    Search books by keywords in description and title, with optional filters.
    Used by recommendation system for more accurate matching.
    
    Args:
        db: Database session
        keywords: List of keywords to search for
        limit: Results per page
        offset: Pagination offset
        author: Optional author filter
        genre: Optional genre filter
    
    Returns:
        Tuple of (books list, total count)
    """
    if not keywords:
        return [], 0
    
    query = select(Book)
    count_query = select(func.count()).select_from(Book)
    filters = []
    
    # Add keyword filters (OR conditions - match any keyword)
    keyword_filters = []
    for keyword in keywords:
        search_term = f"%{keyword.strip()}%"
        keyword_filters.append(
            or_(
                Book.name.ilike(search_term),
                Book.description.ilike(search_term)
            )
        )
    
    if keyword_filters:
        filters.append(or_(*keyword_filters))
    
    # Add author filter if provided
    if author:
        filters.append(Book.author.ilike(f"%{author}%"))
    
    # Add genre filter if provided
    if genre:
        filters.append(Book.genre.ilike(f"%{genre}%"))
    
    # Apply all filters with AND logic
    if filters:
        query = query.where(and_(*filters))
        count_query = count_query.where(and_(*filters))
    
    # Get total count
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # Get paginated results
    query = query.limit(limit).offset(offset)
    result = await db.execute(query)
    books = result.scalars().all()
    
    return books, total