# BOOKSTORE_DB

Async FastAPI bookstore platform with JWT auth, cart management, AI-powered book tools, a browser UI, and a local Groq helper package.

The repository now has three important pieces:

- `backend/` for the API, repositories, services, tests, and backend docs
- `frontend/` for the static UI pages, JavaScript controllers, styles, and assets
- `groq_chatbot_lib/` for the local chatbot helper package used by the backend

## Current Layout

```text
BOOKSTORE_DB/
├── backend/
│   ├── app/
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── Repository/
│   │   ├── dependencies/
│   │   ├── routers/
│   │   ├── services/
│   │   └── utils/
│   ├── books.db
│   ├── poetry.lock
│   ├── pyproject.toml
│   ├── pyrightconfig.json
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   └── ui/
│       ├── assets/
│       ├── css/
│       ├── js/
│       └── pages/
├── groq_chatbot_lib/
├── bookstore_backup.sql
├── docker-compose.yml
├── Dockerfile
├── pyrightconfig.json
└── README.md
```

## Run Locally

```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload
```

The app creates database tables on startup, so there is no separate migration bootstrap script in the repo.

## Run With Docker

From the repository root:

```bash
docker compose up --build
```

The compose file runs PostgreSQL on host port `5433` and FastAPI on host port `8000`.

## Environment Variables

The backend reads settings from `.env`. The current code expects at least:

- `DATABASE_URL`
- `GROQ_API_KEY`
- `GROQ_SYSTEM_PROMPT`
- `BOOK_SEARCH_PROMPT_TEMPLATE`
- `BOOK_RECOMMENDATION_PROMPT_TEMPLATE`
- `BOOK_CHAT_PROMPT_TEMPLATE`
- `BOOK_SUMMARY_PROMPT_TEMPLATE`
- `SECRET_KEY`

Useful optional values include:

- `GROQ_CHAT_MODEL`
- `GROQ_SEARCH_MODEL`
- `GROQ_REQUEST_TIMEOUT_SECONDS`
- `AI_SEARCH_TIMEOUT_SECONDS`
- `AI_RECOMMENDATION_TIMEOUT_SECONDS`
- `AI_SUMMARY_TIMEOUT_SECONDS`
- `CHAT_MEMORY_LIMIT`
- `CHAT_CATALOG_SEARCH_LIMIT`
- `ACCESS_TOKEN_EXPIRE_MINUTES`
- `REFRESH_TOKEN_EXPIRE_DAYS`
- `POSTGRES_USER`
- `POSTGRES_PASSWORD`
- `POSTGRES_DB`

The prompt template variables support `[[placeholder]]` tokens, which are replaced at runtime by the backend services.

## API And UI

API docs:

- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

Core API routes:

- `GET /` returns the health-style welcome response
- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`
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
- `POST /chat`
- `GET /carts`
- `POST /carts/add`
- `PUT /carts/update/{item_id}`
- `DELETE /carts/delete/{item_id}`
- `DELETE /carts/clear`

Frontend pages under `/ui`:

- `/ui`
- `/ui/login`
- `/ui/register`
- `/ui/dashboard`
- `/ui/profile`
- `/ui/chatbot`
- `/ui/shop`
- `/ui/product?id={book_id}`
- `/ui/books/write`
- `/ui/books/edit`
- `/ui/books/view`
- `/ui/books/search`
- `/ui/books/ai-search`
- `/ui/books/ai-summary`
- `/ui/books/ai-recommendations`

## Notes

- The BookGPT chat endpoint is authenticated and uses the real catalog before returning a response.
- The backend depends on the local `groq_chatbot_lib/` package in this repository.
- The top-level `pyrightconfig.json` is already configured for the workspace layout and the local package.
- `bookstore_backup.sql` is the current SQL backup artifact for the project.

For backend implementation details, see `backend/README.md`.
