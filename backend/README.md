# Backend

FastAPI backend for BOOKSTORE_DB. The app is asynchronous end to end and uses SQLAlchemy, PostgreSQL, JWT auth, a cart workflow, AI-powered book endpoints, and an authenticated chatbot grounded on the live catalog.

## What Lives Here

- `app/main.py` wires routers, static UI mounting, and startup table creation.
- `app/routers/` exposes auth, books, carts, and chat endpoints.
- `app/services/` contains auth logic, book operations, AI helpers, and chatbot orchestration.
- `app/Repository/` contains the database access layer.
- `app/utils/groq_client.py` bridges the backend to the local Groq helper package.
# Backend

FastAPI backend for BOOKSTORE_DB. The app is asynchronous end to end and uses SQLAlchemy, PostgreSQL, JWT auth, a cart workflow, AI-powered book endpoints, and an authenticated chatbot grounded on the live catalog.

## What Lives Here

- `app/main.py` wires routers, static UI mounting, and startup table creation.
- `app/routers/` exposes auth, books, carts, and chat endpoints.
- `app/services/` contains auth logic, book operations, AI helpers, and chatbot orchestration.
- `app/Repository/` contains the database access layer.
- `app/utils/groq_client.py` bridges the backend to the local Groq helper package.
- `../groq_chatbot_lib/` is a local package dependency that ships with this repository.

## Run Locally

```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload
```

The application creates tables on startup through `app.main`, so there is no separate bootstrap script to run.

## Environment Variables

The backend reads environment values from `.env`.

Required for a working app:

- `DATABASE_URL`
- `GROQ_API_KEY`
- `GROQ_SYSTEM_PROMPT`
- `BOOK_SEARCH_PROMPT_TEMPLATE`
- `BOOK_RECOMMENDATION_PROMPT_TEMPLATE`
- `BOOK_CHAT_PROMPT_TEMPLATE`
- `BOOK_SUMMARY_PROMPT_TEMPLATE`
- `SECRET_KEY`

Common optional settings:

- `GROQ_CHAT_MODEL` defaults to `llama-3.1-8b-instant`
- `GROQ_SEARCH_MODEL` defaults to `GROQ_CHAT_MODEL`
- `GROQ_REQUEST_TIMEOUT_SECONDS` defaults to `10`
- `AI_SEARCH_TIMEOUT_SECONDS` defaults to `5`
- `AI_RECOMMENDATION_TIMEOUT_SECONDS` defaults to `5`
- `AI_SUMMARY_TIMEOUT_SECONDS` defaults to `10`
- `CHAT_MEMORY_LIMIT` defaults to `10`
- `CHAT_CATALOG_SEARCH_LIMIT` defaults to `5`
- `ACCESS_TOKEN_EXPIRE_MINUTES` defaults to `60`
- `REFRESH_TOKEN_EXPIRE_DAYS` defaults to `7`
- `POSTGRES_USER`, `POSTGRES_PASSWORD`, `POSTGRES_DB` are used by Docker Compose defaults

Prompt templates support `[[placeholder]]` replacements at runtime. Keep those tokens in the template text when you want the backend to inject values such as query, title, book metadata, or conversation history.

## API Surface

Auth:

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`

Books:

- `GET /books`
- `POST /books`
- `POST /books/bulk`
- `GET /books/{book_id}`
- `PUT /books/{book_id}`
- `DELETE /books/{book_id}`
- `GET /books/search`
- `GET /books/ai-search`
- `GET /books/recommendations`
- `GET /books/summary/search`

Chat:

- `POST /chat`

Cart:

- `GET /carts`
- `POST /carts/add`
- `PUT /carts/update/{item_id}`
- `DELETE /carts/delete/{item_id}`
- `DELETE /carts/clear`

The chatbot endpoint is authenticated and uses the local `groq_chatbot_lib` tool-calling client to resolve catalog lookups, book-by-ID requests, count questions, and recommendations before returning the final reply.

## AI Endpoints

- `GET /books/ai-search` performs natural-language catalog search.
- `GET /books/recommendations` returns catalog-based recommendations for a title.
- `GET /books/summary/search` returns a generated summary by book ID or book name.
- `POST /chat` returns a DB-grounded conversation reply with fields such as `lookup_mode`, `matched_books_count`, and `store_book_count`.

## Docker

```bash
docker compose up --build
```

In Docker Compose, PostgreSQL is exposed on host port `5433` and the API on host port `8000`.

If you run the backend locally against the Compose database, use a `DATABASE_URL` that targets `localhost:5433`. Inside Docker, the database host should be `postgres:5432`.

## Tests

```bash
poetry run pytest
```

## Notes

- The project keeps a local helper package in `../groq_chatbot_lib/`; do not treat it as an external pip-only dependency.
- The workspace-level `pyrightconfig.json` is already configured for the backend and the local helper package.
- The SQL backup file at the repository root is `../bookstore_backup.sql`.
| Method | Endpoint       | Description                        |
|:------:|----------------|------------------------------------|
| POST   | `/books`       | Create a new book *(admin only)*   |
| POST   | `/books/bulk`  | Bulk create multiple books         |
| GET    | `/books`       | Get books (filtering & pagination) |
| GET    | `/books/{id}`  | Get a single book by ID            |
| PUT    | `/books/{id}`  | Update a book *(admin only)*       |
| DELETE | `/books/{id}`  | Delete a book *(admin only)*       |

### 🤖 AI-Powered Features

| Method | Endpoint                 | Description                                  |
|:------:|--------------------------|----------------------------------------------|
| GET    | `/books/search`          | AI-powered book search by query              |
| GET    | `/books/recommend`       | AI-powered book recommendations              |
| GET    | `/books/summary/search`  | AI-generated book summaries (by ID or name)  |
| POST   | `/chat`                  | BookGPT chat with DB-grounded context        |

### 💬 BookGPT Chat

`POST /chat` accepts a user message plus an optional history window, then routes requests through three lookup modes before general generation:

- `store_count`: answers exact count questions from database
- `exact_book_id`: resolves direct ID queries such as "book id 3"
- `catalog_search`: fuzzy-matches titles/authors for typo-tolerant grounding

If no catalog match is found, it falls back to `general_answer` while preserving conversation context.

Request body example:

```json
{
  "message": "do we have the boyfreind?",
  "history_limit": 10
}
```

Response highlights:

- `reply`: assistant response text
- `lookup_mode`: which logic path answered
- `matched_books_count`: number of catalog matches used
- `store_book_count`: returned for count-oriented questions

---

## 🔍 Filtering & Pagination

### Pagination
=======
>>>>>>> Stashed changes
```bash
poetry run pytest
```

## Notes

- The project keeps a local helper package in `../groq_chatbot_lib/`; do not treat it as an external pip-only dependency.
- The workspace-level `pyrightconfig.json` is already configured for the backend and the local helper package.
- The SQL backup file at the repository root is `../bookstore_backup.sql`.
```bash
/books?genre=Fantasy
```

### Filter by Date Range (Flexible Formats)
```bash
# Full date
/books?start_date=2000-01-01&end_date=2020-12-31

# Year only
/books?start_date=2000&end_date=2020

# Year and month
/books?start_date=2000-01&end_date=2020-12
```

### Sorting
```bash
# Sort by name (ascending)
/books?sort_by=name&order=asc

# Sort by published date (descending — default)
/books?sort_by=published_date&order=desc

# Sort by genre
/books?sort_by=genre&order=asc

# Available sort fields: name, author, published_date, genre
# Available orders: asc, desc
```

### Combined Filters & Sorting
```bash
/books?author=Rowling&genre=Fantasy&start_date=1997&end_date=2007&sort_by=name&order=asc&limit=5&offset=0
```

---

## 🤖 AI-Powered Features

### AI Book Search
Search for books using natural language queries:
```bash
GET /books/search?query="books about productivity and habits"
```

### AI Book Recommendations
Get personalized book recommendations:
```bash
GET /books/recommend?query="I want to learn programming"
```

### AI Book Summaries
Generate engaging, story-like summaries of books.

**By Book ID:**
```bash
GET /books/summary/search?id=1
```

**By Book Name:**
```bash
GET /books/summary/search?name=harry%20potter
```

**Response Format:**
```json
{
  "book_id": 1,
  "name": "Harry Potter and the Sorcerer's Stone",
  "author": "J.K. Rowling",
  "summary": "In a world where magic is real but hidden from most people..."
}
```

---

## ⚡ Bulk Insert Example

```json
{
  "books": [
    {
      "name": "string 1",
      "author": "string",
      "genre": "string",
      "published_date": "2026-03-26",
      "description": "string"
    },
    {
      "name": "string 2",
      "author": "string",
      "genre": "string",
      "published_date": "2026-03-26",
      "description": "string"
    }
  ]
}
```

---

## 🧪 Running Tests

```bash
pytest -v
```

---

## 🧩 Error Handling

Centralized using service wrappers; consistent API responses.

Handles:

- ❌ `404` Not Found
- ⚠️ `400` Bad Request
- 💥 `500` Internal Errors

---

## 💡 Key Learnings

- Async FastAPI architecture
- SQLAlchemy async queries
- Clean backend layering
- Pagination & filtering patterns
- **Advanced sorting with SQLAlchemy `order_by()`**
- **Flexible date parsing (year/month/day support)**
- Bulk data handling
- Pydantic v2 migration
- **AI Integration with Groq API**
- **Natural Language Processing for search**
- **Prompt engineering for AI responses**
- **Error handling for external API calls**

---

## 🔮 Future Improvements

- ✅ **AI-Powered Search** (Implemented)
- ✅ **AI Recommendations** (Implemented)
- ✅ **AI Book Summaries** (Implemented)
- ✅ **Advanced Sorting** (Implemented)
- ✅ **Docker Support** (Implemented)
- 🔐 Authentication & authorization
- 🔍 Advanced full-text search
- ⚙️ CI/CD pipeline

---

## 🤝 Contributions

Contributions are welcome!

**Fork → Create branch → Commit → PR 🚀**

---

## ⭐ Final Note

This project demonstrates a production-ready backend structure using modern async Python tools, now enhanced with **cutting-edge AI capabilities** for intelligent book discovery and content generation.

🚀 Built with passion using FastAPI & Groq AI

---

## 📖 Books in Database

- Atomic Habits
- The Alchemist
- Harry Potter and the Sorcerer's Stone
- Harry Potter and the Chamber of Secrets
- Clean Code
- Deep Work
- The Pragmatic Programmer
- Rich Dad Poor Dad
- The Psychology of Money
- Sapiens
- Harry Potter and the Prisoner of Azkaban
- Harry Potter and the Goblet of Fire
- Homo Deus
- The Hobbit
- The Fellowship of the Ring
- The Two Towers
- The Return of the King
- Dune
- 1984
- To Kill a Mockingbird
- The Great Gatsby
- Pride and Prejudice
- The Catcher in the Rye
- The Subtle Art of Not Giving a F*ck
- Can't Hurt Me
- The 7 Habits of Highly Effective People
- Thinking, Fast and Slow
- The Power of Now
- The 5 AM Club
- Grit
- The Four Agreements
- The Body Keeps the Score
- Educated
- Becoming
- The Immortal Life of Henrietta Lacks
- The Martian
- Project Hail Mary
- The Hunger Games
- Catching Fire
- Mockingjay
- Twilight
- New Moon
- Eclipse
- Breaking Dawn
- The Da Vinci Code
- Angels & Demons
- Inferno
- The Girl with the Dragon Tattoo
- The Silent Patient
- Where the Crawdads Sing
- The Night Circus
- The Seven Husbands of Evelyn Hugo
- Daisy Jones & The Six
- Malibu Rising
- The Midnight Library
- The Invisible Life of Addie LaRue
- Circe
- The Song of Achilles
- Verity
- It Ends with Us
- Ugly Love
- November 9
- The Love Hypothesis
- Beach Read
- People We Meet on Vacation
- Book Lovers
- The Housemaid
- Never Lie
- The Maidens
- The Guest List
- The Hunting Party
- The Paris Apartment
- It Starts with Us
- Reminders of Him
- Love on the Brain
- Happy Place
- The Housemaid's Secret
- The Coworker
- The Inmate
- The Locked Door
- Ward D
- The Perfect Son
- One by One
- The Teacher
- The Boyfriend
- The Surrogate Mother
- PEER-E-KAMIL