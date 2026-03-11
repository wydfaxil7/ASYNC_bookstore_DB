# schemas.py
from pydantic import BaseModel
from datetime import date

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

    class Config:
        model_config = {"from_attributes": True}  # replaces orm_mode