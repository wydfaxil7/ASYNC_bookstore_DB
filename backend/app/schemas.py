# schemas.py
from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import date, datetime, timezone
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

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    email: EmailStr
    is_active: bool
    is_admin: bool

    model_config = ConfigDict(from_attributes = True)

class UserLogin(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel): 
    user_id: int | None = None
    username: str | None = None
    is_admin: bool | None = None
    exp: datetime | None = None

class ChatMessage(BaseModel):
    role: str
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class ChatRequest(BaseModel):
    message: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="User message sent to chatbot.",
        examples=["Recommend a fantasy book with strong world-building."]
    )
    history_limit: int = Field(
        default=10,
        ge=1,
        le=20,
        description="How many recent messages to include as context.",
        examples=[10]
    )

class ChatResponse(BaseModel):
    user_id: int
    message: str
    reply: str
    context_used: List[ChatMessage] = Field(default_factory=list)
    message_count: int = 0
    store_book_count: int | None = None
    matched_books_count: int = 0
    lookup_mode: str | None = None
    model_config = ConfigDict(from_attributes=True)
 
