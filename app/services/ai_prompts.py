# app/services/ai_prompts.py

def build_search_prompt(query: str) -> str:
    return f"""
    You are a book database assistant.
    Analyze the user query and respond ONLY with valid JSON.
    The JSON must have the following fields:

    {{
        "intent": "get_author" or "list_books",
        "author": "author name here or null",
        "genre": "genre here or null",
        "start_date": "YYYY-MM-DD or null",
        "end_date": "YYYY-MM-DD or null"
    }}

    Rules:
    - Use quotes around strings.
    - Use null (without quotes) for empty fields.
    - Do NOT add extra text, explanations, or markdown.

    User query: "{query}"
    """