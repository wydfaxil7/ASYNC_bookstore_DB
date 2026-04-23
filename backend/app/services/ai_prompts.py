"""AI prompt templates and shared Groq configuration loaded from .env."""

from __future__ import annotations

import os

from dotenv import load_dotenv

load_dotenv()


def _required_env(name: str) -> str:
    value = os.getenv(name)
    if value is None or not value.strip():
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def render_prompt(template_name: str, **values: str) -> str:
    template = _required_env(template_name)
    for key, value in values.items():
        template = template.replace(f"[[{key}]]", str(value))
    return template.strip()


GROQ_CHAT_MODEL = os.getenv("GROQ_CHAT_MODEL", "llama-3.1-8b-instant")
GROQ_SEARCH_MODEL = os.getenv("GROQ_SEARCH_MODEL", GROQ_CHAT_MODEL)
GROQ_DEFAULT_MODEL = GROQ_SEARCH_MODEL

GROQ_SYSTEM_PROMPT = _required_env("GROQ_SYSTEM_PROMPT")

AI_SEARCH_TIMEOUT_SECONDS = int(os.getenv("AI_SEARCH_TIMEOUT_SECONDS", "5"))
AI_RECOMMENDATION_TIMEOUT_SECONDS = int(os.getenv("AI_RECOMMENDATION_TIMEOUT_SECONDS", "5"))
AI_SUMMARY_TIMEOUT_SECONDS = int(os.getenv("AI_SUMMARY_TIMEOUT_SECONDS", "10"))
GROQ_REQUEST_TIMEOUT_SECONDS = int(os.getenv("GROQ_REQUEST_TIMEOUT_SECONDS", "10"))
CHAT_MEMORY_LIMIT = int(os.getenv("CHAT_MEMORY_LIMIT", "10"))
CHAT_CATALOG_SEARCH_LIMIT = int(os.getenv("CHAT_CATALOG_SEARCH_LIMIT", "5"))


def build_search_prompt(query: str) -> str:
    return render_prompt("BOOK_SEARCH_PROMPT_TEMPLATE", query=query)


def build_recommendation_prompt(title: str) -> str:
    return render_prompt("BOOK_RECOMMENDATION_PROMPT_TEMPLATE", title=title)


def build_chat_prompt(
    user_message: str,
    context: list,
    total_books: int,
    catalog_context: str,
) -> str:
    history_block = ""
    for msg in context:
        role_label = "User" if msg.role == "user" else "Assistant"
        history_block += f"{role_label}: {msg.content}\n"

    return render_prompt(
        "BOOK_CHAT_PROMPT_TEMPLATE",
        user_message=user_message,
        total_books=str(total_books),
        catalog_context=catalog_context,
        history_block=history_block,
    )


def build_summary_prompt(book: dict[str, str]) -> str:
    return render_prompt(
        "BOOK_SUMMARY_PROMPT_TEMPLATE",
        book_name=book.get("book_name", "Not specified"),
        author=book.get("author", "Not specified"),
        genre=book.get("genre", "Not specified"),
        published_date=book.get("published_date", "Not specified"),
        description=book.get("description", "Not specified"),
    )