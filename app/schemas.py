# schemas.py
from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import List

class BookBase(BaseModel):
    name: str
    author: str
    genre: str | None = None
    published_date: date | None = None
    description: str | None = None


class BookCreate(BookBase):
    pass

class BookUpdate(BookBase):
    pass

class BookResponse(BookBase):
    id: int

    model_config = ConfigDict(from_attributes = True)

class BookListResponse(BaseModel):
    total: int
    limit: int
    offset: int
    data: List["BookResponse"]  # List of books
    message: str | None = None  # optional message

    model_config = ConfigDict(from_attributes = True)

class BookBulkCreate(BaseModel):
    books: List[BookCreate]

class BookQueryParams(BaseModel):
    limit: int = 10
    offset: int = 0
    author: str | None = None
    genre: str | None = None
    start_date: str | None = None
    end_date: str | None = None
    sort_by: str | None = None
    order: str | None = None

class AuthorResponse(BaseModel):
    author: str

class AISearchResponse(BaseModel):
    intent: str
    author: str | None = None
    total: int | None = None
    limit: int | None = None
    offset: int | None = None
    data: List[BookResponse] | None = None
    message: str | None = None

class BookSummaryResponse(BaseModel):
    book_id: int
    name: str
    author: str
    summary: str