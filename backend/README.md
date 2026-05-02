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
