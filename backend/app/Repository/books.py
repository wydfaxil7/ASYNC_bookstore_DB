#app/Repository/books.py
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Book
from sqlalchemy import or_, func, and_, asc, desc
from datetime import date
from difflib import SequenceMatcher
import re

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

async def create_bulk_books(db: AsyncSession, books_data: List[dict]):
    """
    Inserts books in bulk
    """
    db_books = [Book(**book) for book in books_data]

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



async def get_books_count(db: AsyncSession) -> int:
    """
    Return exact total number of books in DB
    """
    result = await db.execute(select(func.count()).select_from(Book))
    return int(result.scalar() or 0)

def _normalize_chat_text(value: str) -> str:
    """
    Normalize text for fuzzy matching.
    """
    value = value.lower()
    # Keep letters/numbers/spaces and remove punctuation noise.
    value = re.sub(r"[^a-z0-9\s]", " ", value)
    return " ".join(value.split())


def _informative_tokens(text: str) -> set[str]:
    """
    Extract meaningful tokens by removing common filler words.
    """
    stopwords = {
        "a", "an", "the", "do", "does", "did", "we", "you", "have", "has", "had",
        "is", "are", "was", "were", "in", "on", "of", "for", "to", "with", "by",
        "please", "can", "could", "would", "should", "tell", "me", "about", "book", "books",
        "any", "there", "our", "store", "catalog", "current", "find", "search"
    }
    return {token for token in text.split() if token and token not in stopwords}


def _token_fuzzy_overlap_score(query_tokens: set[str], book_tokens: set[str]) -> float:
    """
    Score typo-tolerant overlap between query tokens and book tokens.
    """
    if not query_tokens or not book_tokens:
        return 0.0

    matched = 0
    for q in query_tokens:
        best = 0.0
        for b in book_tokens:
            best = max(best, SequenceMatcher(None, q, b).ratio())
        if best >= 0.78:
            matched += 1

    return matched / max(len(query_tokens), 1)

def _chat_match_score(query: str, book: Book) -> float:
    """
    Score how well a book matches a human query using fuzzy matching on title and description.
    """
    query_norm = _normalize_chat_text(query)
    title_norm = _normalize_chat_text(book.name)
    author_norm = _normalize_chat_text(book.author)

    # Strong boost for obvious contains matches.
    if query_norm and (query_norm in title_norm or query_norm in author_norm):
        return 1.0

    seq_score = max(
        SequenceMatcher(None, query_norm, title_norm).ratio(),
        SequenceMatcher(None, query_norm, author_norm).ratio()
    )

    query_tokens = _informative_tokens(query_norm)
    book_tokens = _informative_tokens(title_norm + " " + author_norm)

    overlap_score = len(query_tokens & book_tokens) / max(len(query_tokens), 1)
    fuzzy_overlap_score = _token_fuzzy_overlap_score(query_tokens, book_tokens)

    return max(seq_score, overlap_score, fuzzy_overlap_score)

async def search_books_for_chat(
    db: AsyncSession,
    query: str,
    limit: int = 5
) -> list[Book]:
    
    """
    Search books using fuzzy matching for chatbot context. This is a more flexible search that tries to find relevant books even if the query doesn't exactly match titles/authors. It uses a combination of sequence matching and token overlap to score relevance, and returns the top results.
    """
    books = await get_books(db)
    scored_books: list[tuple[float, Book]] = []

    for book in books:
        score = _chat_match_score(query, book)
        if score >= 0.35:
            scored_books.append((score, book))

    scored_books.sort(key=lambda item: item[0], reverse=True)
    return [book for _, book in scored_books[:limit]]



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
                      ) -> tuple[List[Book], int]:
    """
    Search book by title and author, with optional genre filter and pagination
    """

    query = select(Book)
    count_query = select(func.count()).select_from(Book)

    # Search by title OR author
    if q:
        search_term = f"%{q}%"
        predicate = (
            or_(
                Book.name.ilike(search_term),
                Book.author.ilike(search_term)
            )
        )
        query = query.where(predicate)
        count_query = count_query.where(predicate)

    # Filter by Genre
    if genre:
        genre_filter = Book.genre == genre
        query = query.where(genre_filter)
        count_query = count_query.where(genre_filter)

    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
        
    #Pagination
    query = query.offset(offset).limit(limit)
    result = await db.execute(query)
    return result.scalars().all(), total

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