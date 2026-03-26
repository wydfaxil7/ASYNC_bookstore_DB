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