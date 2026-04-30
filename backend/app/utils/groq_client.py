#app/utils/groq_client.py
import os
import json
import re
from groq import Groq
import asyncio
from typing import Dict, Any, Optional

from groq_chatbot_lib import ChatbotClient
from groq_chatbot_lib.extractor import extract_json, extract_json_list

from app.services.ai_prompts import (
    GROQ_CHAT_MODEL,
    GROQ_DEFAULT_MODEL,
    GROQ_REQUEST_TIMEOUT_SECONDS,
    GROQ_SEARCH_MODEL,
    GROQ_SYSTEM_PROMPT,
)

def get_groq_client(model: str = GROQ_DEFAULT_MODEL) -> ChatbotClient:
    """
    Get Groq client with lazy initialization.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set")
    return ChatbotClient(api_key=api_key, model=model)

async def call_groq(
        prompt: str, 
        timeout: int = GROQ_REQUEST_TIMEOUT_SECONDS, 
        model: str = GROQ_DEFAULT_MODEL,
        system_prompt: str = ""
        ) -> str:
    """
    Async wrapper for Groq API with timeout handling.
    
    Args:
        prompt: The prompt to send to the model
        timeout: Timeout in seconds (default 10)
        model: The model to use
        system_prompt: The system prompt to use
    
    Returns:
        Raw response text from the model
    """
    client = get_groq_client(model=model)

    def _call():
        return client.quick_ask(prompt, system_prompt=system_prompt)

    try:
        return await asyncio.wait_for(
            asyncio.to_thread(_call),
            timeout=timeout
        )
    except asyncio.TimeoutError:
        raise asyncio.TimeoutError(f"Groq API call timed out after {timeout}")
    except Exception as exc:
        if model != GROQ_SEARCH_MODEL and "model_decommissioned" in str(exc):
            client_fallback = get_groq_client(model=GROQ_SEARCH_MODEL)
            return await asyncio.to_thread(
                lambda: client_fallback.quick_ask(prompt, system_prompt=system_prompt)
            )
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
    from groq_chatbot_lib.extractor import extract_json_list
    return extract_json_list(response_text)


def extract_json_list_from_response(response_text: str) -> list[Dict[str, Any]]:
    """
    Extract multiple JSON objects from response text.
    
    Args:
        response_text: Raw response from AI
    
    Returns:
        List of parsed JSON objects, empty list if none found
    """
    from groq_chatbot_lib.extractor import extract_json_list
    return extract_json_list(response_text)

async def call_groq_with_json_response(
    prompt: str,
    timeout: int = GROQ_REQUEST_TIMEOUT_SECONDS,
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
        client = get_groq_client()
        response = await asyncio.wait_for(
            asyncio.to_thread(lambda: client.quick_ask(prompt)),
            timeout=timeout
        )
        from groq_chatbot_lib.extractor import extract_json, validate_schema
        json_data = extract_json(response)

        if not json_data or not isinstance(json_data,dict):
            return None
        
        # Validate required fields
        if required_fields:
            if not validate_schema(json_data, required_fields):
                return None
            
        return json_data
    except asyncio.TimeoutError:
        return None
    except Exception:
        return None