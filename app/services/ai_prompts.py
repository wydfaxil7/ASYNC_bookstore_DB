# app/services/ai_prompts.py

def build_search_prompt(query: str) -> str:
    """
    Builds a strict, structured prompt for book search AI.
    Ensures reliable JSON extraction and validation.
    """
    return f"""You are a book search AI assistant for a bookstore database.

Your task: Parse the user's query and return ONLY a valid JSON object with search filters.

IMPORTANT RULES:
1. Return ONLY valid JSON - no markdown, no extra text, no explanations
2. Author MUST be extracted if ANY person/name is mentioned in the query
3. Genre should be realistic book genres (fiction, romance, mystery, sci-fi, etc.)
4. If multiple names/authors mentioned, pick the most relevant one
5. Do NOT return null for author if a name is clearly mentioned

RESPONSE SCHEMA:
{{
    "intent": "get_author" or "list_books",
    "author": "exact author name or null",
    "genre": "book genre or null",
    "keywords": ["relevant keywords from query"],
    "confidence": 0.0 to 1.0
}}

INTENT RULES:
- Use "get_author" only if query asks "who wrote", "author of", or "by whom"
- Use "list_books" for all search/recommendation queries

EXTRACTION EXAMPLES:
- "harry potter books" → author: "J.K. Rowling", intent: "list_books"
- "umair ahmed" → author: "Umair Ahmed", intent: "list_books"
- "romantic novels" → genre: "romance", keywords: ["romantic", "love", "relationship"]
- "sci-fi books by asimov" → author: "Isaac Asimov", genre: "sci-fi"
- "mystery" → genre: "mystery", intent: "list_books"

User query: "{query}"

RESPOND WITH ONLY THE JSON OBJECT:"""


def build_recommendation_prompt(title: str) -> str:
    """
    Builds a prompt for AI-based book recommendations.
    Extracts genre, author patterns, and keywords for database matching.
    """
    return f"""You are a book recommendation AI for a bookstore database.

Given a book title, analyze it and suggest search filters for similar books.

TASK: Return JSON with filters to find similar books.

RESPONSE SCHEMA:
{{
    "primary_genre": "main genre of the book or null",
    "secondary_genres": ["similar genres for recommendations"],
    "author_pattern": "author name or null",
    "keywords": ["themes, topics, keywords from the book"],
    "confidence": 0.0 to 1.0,
    "reason": "brief explanation of recommendations"
}}

EXTRACTION RULES:
1. Identify the primary genre (romance, sci-fi, mystery, fantasy, etc.)
2. List 2-3 similar genres readers might enjoy
3. Extract author if it's a known author, else null
4. Create keyword list (themes, plot elements, character types, etc.)
5. Set confidence level based on how well-known the book is

EXAMPLES:
Book: "The Great Gatsby"
{{
    "primary_genre": "fiction",
    "secondary_genres": ["romance", "historic fiction"],
    "author_pattern": "F. Scott Fitzgerald",
    "keywords": ["wealthy protagonist", "love story", "1920s", "jazz age", "tragedy"],
    "confidence": 0.95
}}

Book: "Harry Potter and the Philosopher's Stone"
{{
    "primary_genre": "fantasy",
    "secondary_genres": ["young adult", "magic"],
    "author_pattern": "J.K. Rowling",
    "keywords": ["wizarding world", "magic school", "coming of age", "adventure"],
    "confidence": 0.98
}}

Book title: "{title}"

RESPOND WITH ONLY THE JSON OBJECT:"""