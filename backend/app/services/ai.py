# app/services/ai.py
import json
import re
import asyncio
from datetime import date
from typing import Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.groq_client import (
    call_groq,
    extract_json_from_response,
    extract_json_list_from_response,
    call_groq_with_json_response
)
from app.Repository import books as repo
from app.services.ai_prompts import (
    AI_RECOMMENDATION_TIMEOUT_SECONDS,
    AI_SEARCH_TIMEOUT_SECONDS,
    AI_SUMMARY_TIMEOUT_SECONDS,
    build_search_prompt,
    build_recommendation_prompt,
)


# HELPER FUNCTIONS FOR JSON EXTRACTION AND VALIDATION

def extract_json(text: str) -> Optional[dict]:
    """
    Extract first valid JSON object from AI response.
    Uses improved groq_client validation.
    """
    return extract_json_from_response(text)


def safe_date_parse(value: str | None) -> date | None:
    """
    Convert string to date safely.
    """
    if not value:
        return None
    try:
        return date.fromisoformat(value)
    except (ValueError, TypeError):
        return None


def validate_search_filters(filters: dict) -> dict:
    """
    Validate and normalize AI-extracted search filters.
    Ensures required fields are present and valid.
    
    Args:
        filters: Raw filters from AI
    
    Returns:
        Validated and normalized filters
    """
    if not filters or not isinstance(filters, dict):
        return {
            "intent": "list_books",
            "author": None,
            "genre": None,
            "keywords": [],
            "confidence": 0.0
        }
    
    return {
        "intent": filters.get("intent", "list_books"),
        "author": filters.get("author"),
        "genre": filters.get("genre"),
        "keywords": filters.get("keywords", []),
        "confidence": float(filters.get("confidence", 0.0))
    }


# AI SEARCH SERVICE

async def ai_search_service(
    db: AsyncSession,
    query: str,
    limit: int = 10,
    offset: int = 0
):
    """
    Perform AI-powered search with DB cross-check and fallback.
    
    Process:
    1. Send query to AI for intent/filter extraction
    2. Validate AI response
    3. Cross-check with database
    4. Return results with pagination
    
    Args:
        db: Database session
        query: User search query
        limit: Results per page
        offset: Pagination offset
    
    Returns:
        Dict with intent, filters, results, and metadata
    """
    prompt = build_search_prompt(query)
    filters = None
    ai_confidence = 0.0
    
    # Try AI extraction
    try:
        response = await asyncio.wait_for(call_groq(prompt), timeout=AI_SEARCH_TIMEOUT_SECONDS)
        print(f"🤖 AI Search Response: {response[:200]}...")
        
        filters = extract_json(response)
        if filters:
            filters = validate_search_filters(filters)
            ai_confidence = filters.get("confidence", 0.0)
    except asyncio.TimeoutError:
        print("⚠️ AI timeout, using fallback")
    except Exception as e:
        print(f"⚠️ AI error: {e}, using fallback")
    
    # Fallback if AI fails
    if not filters or not filters.get("author") and not filters.get("genre"):
        books, total = await repo.search_book(
            db=db,
            q=query,
            genre=None,
            limit=limit,
            offset=offset
        )
        
        return {
            "intent": "list_books",
            "author": None,
            "genre": None,
            "total": total,
            "limit": limit,
            "offset": offset,
            "data": books,
            "message": "Fallback search by title/author",
            "ai_confidence": 0.0
        }
    
    # Extract validated filters
    intent = filters.get("intent", "list_books")
    author = filters.get("author")
    genre = filters.get("genre")
    keywords = filters.get("keywords", [])
    
    # Handle "get_author" intent
    if intent == "get_author" and author:
        return {
            "intent": "get_author",
            "author": author,
            "genre": None,
            "total": 0,
            "limit": limit,
            "offset": offset,
            "data": [],
            "message": f"Author query: {author}",
            "ai_confidence": ai_confidence
        }
    
    # Query database with AI-extracted filters
    books, total = await repo.get_books_with_filters(
        db=db,
        limit=limit,
        offset=offset,
        author=author,
        genre=genre
    )
    
    # If no results and we have keywords, try keyword search
    if not books and keywords:
        books, total = await repo.search_books_by_keywords(
            db=db,
            keywords=keywords,
            limit=limit,
            offset=offset,
            author=author,
            genre=genre
        )
    
    return {
        "intent": intent,
        "author": author,
        "genre": genre,
        "total": total,
        "limit": limit,
        "offset": offset,
        "data": books,
        "message": "Books fetched successfully" if books else "No books found matching criteria",
        "ai_confidence": ai_confidence
    }

# AI SUMMARY GENERATION SERVICE

async def generate_summary(prompt: str) -> str:
    """
    Generate a story-like summary using AI based on the provided prompt.
    
    Args:
        prompt: The prompt containing book details for summary generation
    
    Returns:
        A story-like summary string
    """
    try:
        response = await asyncio.wait_for(call_groq(prompt), timeout=AI_SUMMARY_TIMEOUT_SECONDS)
        # Clean up the response - remove any markdown formatting
        summary = response.strip()
        if summary.startswith("```"):
            summary = re.sub(r"^```[a-zA-Z]*\n?", "", summary)
            summary = re.sub(r"\n?```$", "", summary)
        return summary.strip()
    except asyncio.TimeoutError:
        raise Exception("AI summary generation timed out")
    except Exception as e:
        raise Exception(f"AI summary generation failed: {str(e)}")


def extract_json_list(text: str):
    """
    Extracts one or more JSON objects from a string returned by AI.
    Returns a list of dictionaries.
    """
    json_objects = []
    # Match {...} blocks in the text
    matches = re.findall(r'\{.*?\}', text, re.DOTALL)
    for match in matches:
        try:
            obj = json.loads(match)
            json_objects.append(obj)
        except json.JSONDecodeError:
            continue
    return json_objects

# AI RECOMMENDATION SERVICE

async def ai_recommend_book_service(db: AsyncSession, query_title: str, limit: int = 5, offset: int = 0):
    """
    Recommend books using AI-generated filters and keyword matching.
    
    Process:
    1. Send book title to AI for genre/author/keyword extraction
    2. Use extracted filters for primary recommendation
    3. Apply keyword-based matching for accuracy
    4. Exclude the original book and duplicates
    
    Args:
        db: Database session
        query_title: Book title to recommend from
        limit: Results per page
        offset: Pagination offset
    
    Returns:
        Dict with recommendations and metadata
    """
    prompt = build_recommendation_prompt(query_title)
    books = []
    total = 0
    ai_confidence = 0.0
    message = "No recommendations found"
    
    try:
        response = await asyncio.wait_for(call_groq(prompt), timeout=AI_RECOMMENDATION_TIMEOUT_SECONDS)
        print(f"🤖 AI Recommendation Response: {response[:200]}...")
        
        filters = extract_json(response)
        if not filters or not isinstance(filters, dict):
            filters = {}
        
        ai_confidence = float(filters.get("confidence", 0.0))
        
        # Extract recommendation filters
        primary_genre = filters.get("primary_genre")
        secondary_genres = filters.get("secondary_genres", [])
        author_pattern = filters.get("author_pattern")
        keywords = filters.get("keywords", [])
        
        # Strategy 1: Try primary genre
        if primary_genre:
            books, total = await repo.get_books_with_filters(
                db=db,
                limit=limit * 2,  # Get extra for filtering
                offset=0,
                genre=primary_genre,
                author=None
            )
        
        # Strategy 2: If no results, try author
        if not books and author_pattern:
            books, total = await repo.get_books_with_filters(
                db=db,
                limit=limit * 2,
                offset=0,
                author=author_pattern,
                genre=None
            )
        
        # Strategy 3: Try keyword matching
        if not books and keywords:
            books, total = await repo.search_books_by_keywords(
                db=db,
                keywords=keywords,
                limit=limit * 2,
                offset=0,
                genre=primary_genre,
                author=author_pattern
            )
        
        # Strategy 4: Try secondary genres
        if not books and secondary_genres:
            for sec_genre in secondary_genres:
                books, total = await repo.get_books_with_filters(
                    db=db,
                    limit=limit * 2,
                    offset=0,
                    genre=sec_genre,
                    author=None
                )
                if books:
                    break
        
        # Post-processing: Remove original book and duplicates
        books = [book for book in books if book.name.lower() != query_title.lower()]
        
        # Remove duplicates
        seen = set()
        unique_books = []
        for book in books:
            if book.id not in seen:
                seen.add(book.id)
                unique_books.append(book)
        books = unique_books
        
        # Apply pagination after filtering
        total = len(books)
        books = books[offset:offset + limit]
        
        if books:
            message = f"Recommendations based on {query_title}"
        
    except asyncio.TimeoutError:
        print("⚠️ AI recommendation timeout")
        message = "AI timeout, no recommendations available"
    except Exception as e:
        print(f"⚠️ AI recommendation error: {e}")
        message = f"Error generating recommendations: {str(e)}"
    
    return {
        "total": total,
        "limit": limit,
        "offset": offset,
        "data": books,
        "message": message,
        "ai_confidence": ai_confidence
    }