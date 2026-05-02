# app/services/chatbot.py

import os
from typing import Dict
from sqlalchemy.ext.asyncio import AsyncSession

from groq_chatbot_lib import ChatbotClient
from groq_chatbot_lib.tools import ToolDefinition, ToolParameter, ToolCall, ToolResult
from groq_chatbot_lib.utils import sanitize_message

from app.Repository import books as books_repo
from app.schemas import ChatMessage, ChatRequest, ChatResponse
from app.services.ai_prompts import (
    CHAT_MEMORY_LIMIT,
    GROQ_CHAT_MODEL,
    GROQ_SYSTEM_PROMPT
)


# ── PER-USER BOT INSTANCES ───────────────────────────────────────────────────

_USER_BOTS: Dict[int, ChatbotClient] = {}
_GROQ_API_KEY = os.getenv("GROQ_API_KEY")


def _get_or_create_bot(user_id: int) -> ChatbotClient:
    if user_id not in _USER_BOTS:
        if not _GROQ_API_KEY:
            raise ValueError("GROQ_API_KEY not set")
        bot = ChatbotClient(api_key=_GROQ_API_KEY, model=GROQ_CHAT_MODEL)
        bot.set_system_prompt(GROQ_SYSTEM_PROMPT)
        bot.set_memory_limit(CHAT_MEMORY_LIMIT * 2)
        _USER_BOTS[user_id] = bot
    return _USER_BOTS[user_id]


# ── TOOL DEFINITIONS ─────────────────────────────────────────────────────────

BOOKSTORE_TOOLS = [

    ToolDefinition(
        name="search_books",
        description=(
            "Search the bookstore catalog by title, author, genre, or keyword. "
            "Use this when the user asks to find, browse, or look for books. "
            "If no results are found, tell the user the book was not found. "
            "Do NOT guess or invent book IDs. Only use IDs returned by this tool."
        ),
        parameters=[
            ToolParameter(
                name="query",
                type="string",
                description="The search term — a title, author name, genre, or topic. Can be empty if searching by genre only.",
                required=False
            ),
            ToolParameter(
                name="genre",
                type="string",
                description="Optional genre filter such as fantasy, sci-fi, romance, thriller",
                required=False
            )
        ]
    ),

    ToolDefinition(
        name="get_book_by_id",
        description=(
            "Fetch full details of one specific book using its ID number. "
            "Use this when the user mentions a book ID or asks about a specific numbered book."
        ),
        parameters=[
            ToolParameter(
                name="book_id",
                type="integer",
                description="The numeric ID of the book to retrieve",
                required=True
            )
        ]
    ),

    ToolDefinition(
        name="count_books",
        description=(
            "Return the total number of books in the store. "
            "Use this when the user asks how many books exist or the total count."
        ),
        parameters=[]
    ),

    ToolDefinition(
        name="get_recommendations",
        description=(
            "Recommend books similar to a given title. "
            "Use this when the user asks for recommendations or what to read next."
        ),
        parameters=[
            ToolParameter(
                name="title",
                type="string",
                description="The book title to base recommendations on",
                required=True
            )
        ]
    )

]


# ── EXECUTOR FACTORY ─────────────────────────────────────────────────────────

def make_executor(db: AsyncSession, total_books: int):
    """
    Returns an async executor function with db and total_books baked in.
    This is a closure — inner function remembers outer variables.
    """

    async def executor(tool_call: ToolCall) -> ToolResult:

        name = tool_call.name
        args = tool_call.arguments

        if name == "search_books":
            query = args.get("query", "")
            genre = args.get("genre", None)

            try:
                books, total = await books_repo.search_book(
                    db=db,
                    q=query,
                    genre=genre,
                    limit=5,
                    offset=0
                )

                if not books:
                    return ToolResult(
                        tool_call_id=tool_call.id,
                        content=f"No books found matching '{query}'."
                    )

                lines = [f"Found {total} book(s) matching '{query}':\n"]
                for i, book in enumerate(books, 1):
                    lines.append(
                        f"{i}. \"{book.name}\" by {book.author} "
                        f"(Genre: {book.genre or 'General'}, ID: {book.id})"
                    )

                return ToolResult(
                    tool_call_id=tool_call.id,
                    content="\n".join(lines)
                )

            except Exception as e:
                return ToolResult(
                    tool_call_id=tool_call.id,
                    content=f"Search failed: {str(e)}",
                    is_error=True
                )

        elif name == "get_book_by_id":
            book_id = args.get("book_id")

            if book_id is None:
                return ToolResult(
                    tool_call_id=tool_call.id,
                    content="No book ID was provided.",
                    is_error=True
                )

            try:
                book = await books_repo.get_book(db, book_id)

                if not book:
                    return ToolResult(
                        tool_call_id=tool_call.id,
                        content=f"No book found with ID {book_id}."
                    )

                published = str(book.published_date) if book.published_date else "Unknown"
                description = book.description or "No description available."

                return ToolResult(
                    tool_call_id=tool_call.id,
                    content=(
                        f"Book ID {book.id}: \"{book.name}\" by {book.author}\n"
                        f"Genre: {book.genre or 'General'} | Published: {published}\n"
                        f"{description}"
                    )
                )

            except Exception as e:
                return ToolResult(
                    tool_call_id=tool_call.id,
                    content=f"Book lookup failed: {str(e)}",
                    is_error=True
                )

        elif name == "count_books":
            return ToolResult(
                tool_call_id=tool_call.id,
                content=f"The bookstore currently has {total_books} books in its catalog."
            )

        elif name == "get_recommendations":
            title = args.get("title", "")

            try:
                books, total = await books_repo.get_books_with_filters(
                    db=db,
                    limit=5,
                    offset=0,
                    author=None,
                    genre=None
                )

                books = [b for b in books if b.name.lower() != title.lower()]

                if not books:
                    return ToolResult(
                        tool_call_id=tool_call.id,
                        content=f"No recommendations found similar to '{title}'."
                    )

                lines = [f"Books you might enjoy if you liked '{title}':\n"]
                for i, book in enumerate(books, 1):
                    lines.append(
                        f"{i}. \"{book.name}\" by {book.author} "
                        f"(Genre: {book.genre or 'General'}, ID: {book.id})"
                    )

                return ToolResult(
                    tool_call_id=tool_call.id,
                    content="\n".join(lines)
                )

            except Exception as e:
                return ToolResult(
                    tool_call_id=tool_call.id,
                    content=f"Recommendations failed: {str(e)}",
                    is_error=True
                )

        else:
            return ToolResult(
                tool_call_id=tool_call.id,
                content=f"Unknown tool '{name}' was requested.",
                is_error=True
            )

    return executor


# ── HISTORY CONVERTER ────────────────────────────────────────────────────────

def _bot_history_to_chat_messages(bot: ChatbotClient, limit: int) -> list[ChatMessage]:
    recent = bot.get_recent_history(limit)
    return [
        ChatMessage(role=m["role"], content=m["content"])
        for m in recent
        if m["role"] in ("user", "assistant")
    ]


# ── MAIN CHAT HANDLER ────────────────────────────────────────────────────────

async def build_chat_turn(
        db: AsyncSession,
        current_user: dict,
        payload: ChatRequest,
) -> ChatResponse:

    user_id = current_user["user_id"]

    try:
        user_message = sanitize_message(payload.message)
    except ValueError:
        user_message = payload.message.strip()

    bot = _get_or_create_bot(user_id)
    total_books = await books_repo.get_books_count(db)
    executor = make_executor(db, total_books)

    reply = await bot.ask_with_tools(
        user_message=user_message,
        tools=BOOKSTORE_TOOLS,
        executor=executor
    )

    context_used = _bot_history_to_chat_messages(bot, payload.history_limit)

    return ChatResponse(
        user_id=user_id,
        message=user_message,
        reply=reply,
        context_used=context_used,
        message_count=bot.count_turns(),
        store_book_count=total_books,
        matched_books_count=0,
        lookup_mode="tool_calling"
    )