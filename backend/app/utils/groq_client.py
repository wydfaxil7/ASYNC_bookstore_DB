#app/utils/groq_client.py
import os
import json
import re
from groq import Groq
import asyncio
from typing import Dict, Any, Optional

GROQ_CHAT_MODEL = os.getenv("GROQ_CHAT_MODEL", "llama-3.1-8b-instant")
GROQ_SEARCH_MODEL = "llama-3.1-8b-instant"
GROQ_DEFAULT_MODEL = GROQ_SEARCH_MODEL

def get_groq_client() -> Groq:
    """Get Groq client with lazy initialization."""
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set")
    return Groq(api_key=api_key)

async def call_groq(prompt: str, timeout: int = 10, model: str = GROQ_DEFAULT_MODEL) -> str:
    """
    Async wrapper for Groq API with timeout handling.
    
    Args:
        prompt: The prompt to send to the model
        timeout: Timeout in seconds (default 10)
    
    Returns:
        Raw response text from the model
    """
    def _call(selected_model: str):
        client = get_groq_client()
        response = client.chat.completions.create(
            model=selected_model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Respond with valid JSON when requested."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=1024
        )
        return response.choices[0].message.content

    try:
        return await asyncio.to_thread(_call, model)
    except Exception as exc:
        # If a selected model is deprecated/decommissioned, retry once with the stable fallback.
        if model != GROQ_SEARCH_MODEL and "model_decommissioned" in str(exc):
            return await asyncio.to_thread(_call, GROQ_SEARCH_MODEL)
        raise


def extract_json_from_response(response_text: str) -> Optional[Dict[str, Any]]:
    """
    Safely extract and validate JSON from AI response.
    Handles markdown code blocks and invalid formatting.
    
    Args:
        response_text: Raw response from AI
    
    Returns:
        Parsed JSON dict or None if invalid
    """
    if not response_text or not isinstance(response_text, str):
        return None
    
    text = response_text.strip()
    
    # Remove markdown code blocks
    if text.startswith("```"):
        text = re.sub(r"^```(?:json|python)?\n?", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\n?```$", "", text)
        text = text.strip()
    
    # Try direct JSON parsing first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Try to find JSON object in the text
    matches = re.findall(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text, re.DOTALL)
    for match in matches:
        try:
            return json.loads(match)
        except json.JSONDecodeError:
            continue
    
    return None


def extract_json_list_from_response(response_text: str) -> list[Dict[str, Any]]:
    """
    Extract multiple JSON objects from response text.
    
    Args:
        response_text: Raw response from AI
    
    Returns:
        List of parsed JSON objects, empty list if none found
    """
    if not response_text or not isinstance(response_text, str):
        return []
    
    text = response_text.strip()
    
    # Remove markdown code blocks
    if text.startswith("```"):
        text = re.sub(r"^```(?:json|python)?\n?", "", text, flags=re.IGNORECASE)
        text = re.sub(r"\n?```$", "", text)
        text = text.strip()
    
    json_objects = []
    matches = re.findall(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text, re.DOTALL)
    
    for match in matches:
        try:
            obj = json.loads(match)
            if isinstance(obj, dict):
                json_objects.append(obj)
        except json.JSONDecodeError:
            continue
    
    return json_objects


async def call_groq_with_json_response(
    prompt: str,
    timeout: int = 10,
    required_fields: Optional[list[str]] = None
) -> Optional[Dict[str, Any]]:
    """
    Call Groq API and extract/validate JSON response.
    
    Args:
        prompt: The prompt to send
        timeout: Timeout in seconds
        required_fields: Fields that must be present in response
    
    Returns:
        Validated JSON dict or None if extraction/validation fails
    """
    try:
        response = await asyncio.wait_for(call_groq(prompt, timeout), timeout=timeout)
        json_data = extract_json_from_response(response)
        
        if not json_data or not isinstance(json_data, dict):
            return None
        
        # Validate required fields
        if required_fields:
            if not all(field in json_data for field in required_fields):
                return None
        
        return json_data
    except asyncio.TimeoutError:
        return None
    except Exception:
        return None