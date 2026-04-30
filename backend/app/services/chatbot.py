import re
import os
from collections import defaultdict, deque
from datetime import datetime, timezone
from typing import Deque, Dict, List
from sqlalchemy.ext.asyncio import AsyncSession

from groq_chatbot_lib import ChatbotClient
from groq_chatbot_lib.utils import sanitize_message

from app.Repository import books as books_repo
from app.schemas import ChatMessage, ChatRequest, ChatResponse
from app.services.ai_prompts import(
    CHAT_CATALOG_SEARCH_LIMIT,
    CHAT_MEMORY_LIMIT,
    GROQ_CHAT_MODEL,
    GROQ_SYSTEM_PROMPT
)


# ----- 1 ChatBotClient per user -----

_USER_BOTS: Dict[int, ChatbotClient] = {}

_GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def _get_or_create_bot(user_id: int) -> ChatbotClient:
    """
    return existing Chatbotclient for this user or create a fresh one.
    Initialized with bookstre system prompt and memory limit.
    """
    if user_id not in _USER_BOTS:
        if not _GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not set")
        bot = ChatbotClient(api_key=_GROQ_API_KEY, model=GROQ_CHAT_MODEL)
        bot.set_system_prompt(GROQ_SYSTEM_PROMPT)
        bot.set_memory_limit(CHAT_MEMORY_LIMIT * 2)
        _USER_BOTS[user_id] = bot
    return _USER_BOTS[user_id]

# ----- GENERAL QUESTIONS DETECTION -----

_GENERAL_PATTERNS = [
    r"^(hi|hello|hey|howdy|greetings|sup|what'?s up)\b",
    r"^how are you",
    r"^who are you",
    r"^what (are|can) you do",
    r"^(good|bad|okay|ok|fine|thanks|thank you|thx|ty)\b",
    r"^what is \d+",
    r"^(what|who|when|where|why|how) (is|are|was|were|does|do|did) (?!.*book)",
    r"^tell me (a joke|something|about yourself)",
    r"^(help|what can you help|what do you do)"
]

_GENERAL_RE = [re.compile(p, re.IGNORECASE) for p in _GENERAL_PATTERNS]

def is_general_question(message: str) -> bool:
    """
    Returns True if message is general conversation, not book-related.
    Skips DB search for these entirely.
    """
    normalized = message.strip().lower()
    return any (pattern.search(normalized) for pattern in _GENERAL_RE)

# ----- COUNT QUESTION DETETCTION -----

_COUNT_PATTERNS = [
    "how many books",
    "how many do you have",
    "total books",
    "book count",
    "exact count",
    "number of books",
    "how many items",
]

def is_count_question(message: str) -> bool:
    """
    Returns True if message is asking for a count of books in the store.
    This is a common question that can be answered with a fast DB query instead of calling the model.
    """
    normalized = message.strip().lower()
    return any(p in normalized for p in _COUNT_PATTERNS)

# ----- BOOK ID EXTRACTION -----

_BOOK_ID_RE = re.compile(
    r"\b(?:"
    r"book\s*(?:id|number|no\.?)?\s*#?\s*(\d+)"        # "book id 5", "book 5", "book #5"
    r"|id\s*#?\s*(\d+)"                                  # "id 5", "id #5"  
    r"|#\s*(\d+)"                                        # "#5"
    r"|(?:about|find|get|show|details\s+of|info\s+on)\s+(?:book\s+#?)?(\d+)"  # "about 5", "about book 5"
    r"|tell\s+me\s+about\s+(?:book\s+#?)?(\d+)"         # "tell me about 5"
    r")\b",
    re.IGNORECASE
)

def extract_requested_book_id(message: str) -> int | None:
    """
    Search for patterns like "book id 123", "id 123", "#123", "about book 123", "find book #123", etc.
    Returns the extracted book ID as an integer, or None if no valid ID is found.
    """
    match = _BOOK_ID_RE.search(message)
    if match:
        # Return first non-None group
        number = next((g for g in match.groups() if g is not None), None)
        if number:
            return int(number)
    if message.strip().isdigit():
        return int(message.strip())
    return None

# ----- CATALOG FORMATTER -----

def format_catalog_context(matched_books) -> str:
    """
    Convert matched books into clean natural language for Goq.
    Old format was pipe-seperated backend text - Groq echoed it but ugly.
    New format is natural pose that Groq reads and responds naturally
    """
    if not matched_books:
        return "No matching books were found in the store catalog."

    lines = ["Here are some relevant books from our catalog:\n"]
    for i, book in enumerate(matched_books, 1):
        genre = book.genre or "General"
        published = str(book.published_date) if book.published_date else "unknown"
        description = book.description or "No description available"
        if len(description) > 200:
            description = description[:200] + "..."

        lines.append(
            f"{i}.\"{book.name}\" by {book.author}\n"
            f"   Genre: {genre} | Published: {published}\n"
            f"   {description}\n"
        )
    
    return "\n".join(lines)


# ----- HISTORY CONVERTER -----

def _bot_history_to_chat_messages(bot: ChatbotClient, limit: int) -> list[ChatMessage]:
    """
    Convert library history format to ChatMessage schema
    for the ChatResponse context_used field.
    """
    recent = bot.get_recent_history(limit)
    return [
        ChatMessage(
            role = m["role"], 
            content = m["content"]
            )
            for m in recent
            if m["role"] in ("user", "assistant")
    ]


# ----- MAIN CHAT HANDLER -----

async def build_chat_turn(
        db: AsyncSession,
        current_user: dict,
        payload: ChatRequest,
) -> ChatResponse:
    """
    Handles one full chat turn.
    Detects message type, routes to correct handler, returns clean reply
    """
    user_id = current_user["user_id"]

    try: 
        user_message = sanitize_message(payload.message)
    except ValueError:
        user_message = payload.message.strip()

    bot = _get_or_create_bot(user_id)
    total_books = await books_repo.get_books_count(db)


    # ---- CASE 1: Count question

    if is_count_question(user_message):
        reply = f"We currently have {total_books} books in our store catalog."
        bot.inject_context("user", user_message)
        bot.inject_context("assistant", reply)
        context_used = _bot_history_to_chat_messages(bot, payload.history_limit)

        return ChatResponse(
            user_id = user_id,
            message = user_message,
            reply = reply,
            context_used = context_used,
            message_count = bot.count_turns(),
            store_book_count = total_books,
            matched_books_count = 0,
            lookup_mode = "store count",
        )


    # --- CASE 2: Book ID lookup

    requested_book_id = extract_requested_book_id(user_message)
    if requested_book_id is not None:
        book = await books_repo.get_book(db, requested_book_id)

        if book:
            genre = book.genre or "General"
            published = str(book.published_date) if book.published_date else "Unknown"
            description = book.description or "No description available"
            reply = (
                f"Here's what i found for Book #{book.id}:\n\n"
                f"\"{book.name}\" by {book.author}\n"
                f"Genre: {genre} | Published: {published}\n\n"
                f"{description}"
            )    
            lookup_mode = "extract_book_id"
            matched_count = 1
        else:
            reply = f"I couldn't find any book with ID {requested_book_id} in our catalog."
            lookup_mode = "book_id_not_found"
            matched_count = 0
        
        bot.inject_context("user", user_message)
        bot.inject_context("assistant", reply)
        context_used = _bot_history_to_chat_messages(bot, payload.history_limit)

        return ChatResponse(
            user_id = user_id,
            message = user_message,
            reply = reply,
            context_used = context_used,
            message_count = bot.count_turns(),
            store_book_count = total_books,
            matched_books_count = matched_count,
            lookup_mode = lookup_mode,
        )
    

    # --- CASE 3: General Question

    if is_general_question(user_message):
        reply = bot.ask(user_message)
        context_used = _bot_history_to_chat_messages(bot, payload.history_limit)

        return ChatResponse(
            user_id=user_id,
            message=user_message,
            reply=reply,
            context_used=context_used,
            message_count=bot.count_turns(),
            store_book_count=total_books,
            matched_books_count=0,
            lookup_mode="general_answer",
        )
    

    # --- CASE 4: Book_related_question

    matched_books = await books_repo.search_books_for_chat(
        db, user_message, limit=CHAT_CATALOG_SEARCH_LIMIT
    )
    catalog_context = format_catalog_context(matched_books)

    if matched_books:
        bot.inject_context("system", catalog_context)

    reply = bot.ask(user_message)
    context_used = _bot_history_to_chat_messages(bot, payload.history_limit)
    
    return ChatResponse(
        user_id = user_id,
        message = user_message,
        reply = reply,
        context_used = context_used,
        message_count = bot.count_turns(),
        store_book_count = total_books,
        matched_books_count = len(matched_books),
        lookup_mode = "catalog_search" if matched_books else "general_answer"
    )