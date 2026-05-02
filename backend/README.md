# Backend

FastAPI backend for BOOKSTORE_DB. The app is asynchronous end to end and uses SQLAlchemy, PostgreSQL, JWT auth, a cart workflow, AI-powered book endpoints, and an authenticated chatbot grounded on the live catalog.

## Features

- ⚡ Fully asynchronous FastAPI endpoints
- 🗄️ Async SQLAlchemy with PostgreSQL
- 🧱 Clean architecture (Router → Service → Repository)
- 📚 Full CRUD operations on books
- 📄 Pagination with total count (`limit`, `offset`)
- 🔍 Dynamic filtering by author, genre, and published date range
- 🔀 Advanced sorting by name, author, published_date, or genre (asc/desc)
- 📦 Bulk book creation endpoint
- 🛡️ JWT authentication & admin-only protections
- 🤖 AI-Powered Features: search, recommendations, summaries, and BookGPT chat
- 🛒 Cart management with inventory-aware stock reservation
- 🧠 Pydantic v2 schemas
- 🐳 Fully Dockerized (API + PostgreSQL)

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

## BookGPT Chat

`POST /chat` accepts a user message plus an optional history window, then routes requests through lookup modes before general generation:

- `store_count`: answers exact count questions from the database
- `exact_book_id`: resolves direct ID queries such as "book id 3"
- `catalog_search`: fuzzy-matches titles/authors for typo-tolerant grounding

If no catalog match is found, it falls back to `general_answer` while preserving conversation context.

Request body example:

```json
{
  "message": "do we have the boyfriend?",
  "history_limit": 10
}
```

Response highlights:

- `reply`: assistant response text
- `lookup_mode`: which logic path answered
- `matched_books_count`: number of catalog matches used
- `store_book_count`: returned for count-oriented questions

## Cart And Inventory

- Cart operations are user-scoped via JWT auth.
- Cart totals include `total_items` and `total_price`.
- Book stock is adjusted on add/update/delete/clear cart operations.

## AI Endpoints

- `GET /books/ai-search` performs natural-language catalog search.
- `GET /books/recommendations` returns catalog-based recommendations for a title.
- `GET /books/summary/search` returns a generated summary by book ID or book name.
- `POST /chat` returns a DB-grounded conversation reply with fields such as `lookup_mode`, `matched_books_count`, and `store_book_count`.

## Filtering And Pagination

Filter by genre:

```bash
/books?genre=Fantasy
```

Filter by date range (supports year, year-month, or full date):

```bash
/books?start_date=2000&end_date=2020
/books?start_date=2000-01&end_date=2020-12
/books?start_date=2000-01-01&end_date=2020-12-31
```

Sorting:

```bash
/books?sort_by=name&order=asc
/books?sort_by=published_date&order=desc
```

Combined:

```bash
/books?author=Rowling&genre=Fantasy&start_date=1997&end_date=2007&sort_by=name&order=asc&limit=5&offset=0
```

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
