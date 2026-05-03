import json
import re
from typing import Optional


def extract_json(text: str) -> Optional[dict]:
    if not text or not isinstance(text, str):
        return None

    cleaned = text.strip()

    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json|python)?\n?", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\n?```$", "", cleaned)
        cleaned = cleaned.strip()

    try:
        result = json.loads(cleaned)
        if isinstance(result, dict):
            return result
    except json.JSONDecodeError:
        pass

    matches = re.findall(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', cleaned, re.DOTALL)
    for match in matches:
        try:
            result = json.loads(match)
            if isinstance(result, dict):
                return result
        except json.JSONDecodeError:
            continue

    return None


def extract_json_list(text: str) -> list[dict]:
    if not text or not isinstance(text, str):
        return []

    cleaned = text.strip()

    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json|python)?\n?", "", cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r"\n?```$", "", cleaned)
        cleaned = cleaned.strip()

    try:
        result = json.loads(cleaned)
        if isinstance(result, list):
            return [item for item in result if isinstance(item, dict)]
    except json.JSONDecodeError:
        pass

    json_objects = []
    matches = re.findall(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', cleaned, re.DOTALL)
    for match in matches:
        try:
            obj = json.loads(match)
            if isinstance(obj, dict):
                json_objects.append(obj)
        except json.JSONDecodeError:
            continue

    return json_objects


def validate_schema(data: dict, required_keys: list[str]) -> bool:
    if not data or not isinstance(data, dict):
        return False
    return all(key in data for key in required_keys)