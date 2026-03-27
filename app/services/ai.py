import json
import re
import asyncio
from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from app.utils.groq_client import call_groq
from app.Repository import books as repo
from app.services.ai_prompts import build_search_prompt


def extract_json(text: str) -> dict:
    """
    Extract JSON from AI response (handles markdown, text, etc.)
    """
    text = text.strip()

    # Remove starting ```json or ```text etc.
    if text.startswith("```"):
        text = re.sub(r"^```[a-zA-Z]*", "", text)
        text = re.sub(r"```$", "", text)

    # Extract JSON object
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        raise Exception(f"No JSON found in AI response: {text}")

    json_str = match.group()

    try:
        return json.loads(json_str)
    except json.JSONDecodeError as e:
        raise Exception(f"JSON decode error: {json_str}") from e


def safe_date_parse(value: str | None) -> date | None:
    """
    Convert string to date safely. Return None if invalid or null
    """
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


async def ai_search_service(db: AsyncSession, query: str, limit: int, offset: int):
    """
    AI-powered natural language search for books.
    Converts user query → structured filters → calls repository
    """
    # 1️⃣ Build prompt
    prompt = build_search_prompt(query)

    # 2️⃣ Call AI (async-safe)
    try:
        response = await asyncio.wait_for(call_groq(prompt), timeout=5)
    except asyncio.TimeoutError:
        raise Exception("AI Timeout")

    # 3️⃣ Parse JSON safely
    filters = extract_json(response)

    # 4️⃣ Extract + validate intent + filters
    intent = filters.get("intent")  # NEW
    author = filters.get("author")
    genre = filters.get("genre")
    start_date = safe_date_parse(filters.get("start_date"))
    end_date = safe_date_parse(filters.get("end_date"))
    
    # 5️⃣ Handle intent
    if intent == "get_author":
        # Return only author
        return {"author": author}
    
    # Otherwise, return full book list
    books, total = await repo.get_books_with_filters(
        db=db,
        limit=limit,
        offset=offset,
        author=author,
        genre=genre,
        start_date=start_date,
        end_date=end_date
    )
    
    return books, total