import re
from collections import defaultdict, deque
from datetime import datetime, timezone
from typing import Deque, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession

from app.Repository import books as books_repo
from app.schemas import ChatMessage, ChatRequest, ChatResponse
from app.services.ai_prompts import CHAT_CATALOG_SEARCH_LIMIT, CHAT_MEMORY_LIMIT, build_chat_prompt
from app.utils.groq_client import call_groq, GROQ_CHAT_MODEL

CHAT_MEMORY: Dict[int, Deque[ChatMessage]] = defaultdict(
    lambda: deque(maxlen = CHAT_MEMORY_LIMIT)
    )

def normalize_message(message:str) -> str:
    """
    Cleans the input message by:
       -Stripping leading and trailing whitespace
       -accidental formatting issues
    """
    return " ".join(message.strip().split())

def get_recent_context(user_id: int, limit: int) -> List[ChatMessage]:
    """
    Returns only the last few turns for context
    """
    history = list(CHAT_MEMORY[user_id])
    return history[-limit:]

def remember_message(user_id: int, role: str, content: str) -> None:
    """
    Stores a message in the user's chat history
    """
    CHAT_MEMORY[user_id].append(
        ChatMessage(
            role = role,
            content = content, 
            created_at = datetime.now(timezone.utc)
        )
    )

BOOK_ID_PATTERN = re.compile(r"(?:book\s*id|id|#)\s(\d+)", re.IGNORECASE)

def extract_requested_book_id(message: str) -> int | None:
    """
    Extract a book Id from a user message
    """

    match = BOOK_ID_PATTERN.search(message)
    if match: 
        return int(match.group(1))

    if message.strip().isdigit():
        return int(message.strip())

    return None

def is_count_question(message: str) -> bool:
    """
    Detect questions asking for the total number of books.
    """
    normalized = normalize_message(message).lower()
    patterns = [
        "how many books",
        "how many do you have",
        "how many books do you have",
        "total books",
        "book count",
        "exact count",
        "exact figure",
        "number of books",
        "how many items",
    ]
    return any(pattern in normalized for pattern in patterns)

def format_catalog_context(matched_books) -> str:
    """
    Convert matched books into prompt-safe text block
    """
    if not matched_books:
        return "No matching books found in the current catalog."

    lines = []
    for book in matched_books:
        lines.append(
            f"#{book.id} | {book.name} | {book.author} | "
            f"genre={book.genre or '—'} | "
            f"published={book.published_date or '—'} | "
            f"description={book.description or 'No description available.'}"
        )
    
    return "\n".join(lines)


async def fetch_catalog_context(db: AsyncSession, user_message: str, limit: int = CHAT_CATALOG_SEARCH_LIMIT) -> List[dict]:
    """
    Fetch a small set of relevant books from the bookstore DB to ground.
    """
    books, _total = await books_repo.search_book(
        db = db,
        q = user_message,
        genre = None,
        limit = limit,
        offset = 0
    )

    context_rows: List[dict] = []
    for book in books:
        context_rows.append(
            {
                "id": book.id,
                "name": book.name,
                "author": book.author,
                "genre": book.genre,
                "published_date": str(book.published_date) if book.published_date else None,
                "description": book.description
            }
        )

    return context_rows

async def build_chat_turn(
        db: AsyncSession,
        current_user: dict, 
        payload: ChatRequest
) -> ChatResponse:
    """
    Builds a chat turn with both conversation memeory
    grounded DB context
    fuzzy catalog search
    groq fallback for general questions
    """
    user_id = current_user["user_id"]
    user_message = normalize_message(payload.message)
    context = get_recent_context(user_id, payload.history_limit)

    remember_message(user_id, "user", user_message)

    total_books = await books_repo.get_books_count(db)

    if is_count_question(user_message):
        assistant_reply = f"We currently have {total_books} books in the store catalog."
        cleaned_reply = assistant_reply.strip()
        remember_message(user_id, "assistant", cleaned_reply)

        return ChatResponse(
            user_id=user_id,
            message=user_message,
            reply=cleaned_reply,
            context_used=context,
            message_count=len(context),
            store_book_count=total_books,
            matched_books_count=0,
            lookup_mode="store_count",
        )

    requested_book_id = extract_requested_book_id(user_message)
    if requested_book_id is not None:
        book = await books_repo.get_book(db, requested_book_id)

        if book:
            assistant_reply = (
                f"Book #{book.id}: {book.name} by {book.author}. "
                f"Genre: {book.genre or '—'}. "
                f"Published: {book.published_date or '—'}. "
                f"Description: {book.description or 'No description available.'}"
            )
            lookup_mode = "exact_book_id"
            matched_books_count = 1
        else:
            assistant_reply = f"I could not find a book with ID {requested_book_id} in the current catalog."
            lookup_mode = "book_id_not_found"
            matched_books_count = 0

        cleaned_reply = assistant_reply.strip()
        remember_message(user_id, "assistant", cleaned_reply)

        return ChatResponse(
            user_id=user_id,
            message=user_message,
            reply=cleaned_reply,
            context_used=context,
            message_count=len(context),
            store_book_count=total_books,
            matched_books_count=matched_books_count,
            lookup_mode=lookup_mode,
        )

    matched_books = await books_repo.search_books_for_chat(db, user_message, limit=CHAT_CATALOG_SEARCH_LIMIT)
    catalog_context = format_catalog_context(matched_books)
    prompt = build_chat_prompt(user_message, context, total_books, catalog_context)

    assistant_reply = await call_groq(prompt, model=GROQ_CHAT_MODEL)
    cleaned_reply = assistant_reply.strip()
    remember_message(user_id, "assistant", cleaned_reply)

    return ChatResponse(
        user_id=user_id,
        message=user_message,
        reply=cleaned_reply,
        context_used=context,
        message_count=len(context),
        store_book_count=total_books,
        matched_books_count=len(matched_books),
        lookup_mode="catalog_search" if matched_books else "general_answer",
    )
    
    # catalog_context = await fetch_catalog_context(db, user_message)
    # prompt = build_chat_prompt(user_message, context, catalog_context)
    
    # assistant_reply = await call_groq(prompt, model=GROQ_CHAT_MODEL)
    # cleaned_reply = assistant_reply.strip()
    # remember_message(user_id, "assistant", cleaned_reply)

    # return ChatResponse(
    #     user_id = user_id,
    #     message = user_message,
    #     reply = cleaned_reply,
    #     context_used = context,
    #     message_count = len(context)
    # )