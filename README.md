# ASYNC Bookstore DB

Async FastAPI bookstore API + modular frontend UI.

Project is split into:

- `backend/` for API, business logic, and tests
- `frontend/` for pages, JS controllers, styles, and assets

## Full Folder Structure

```text
BOOKSTORE_DB/
├── .dockerignore
├── .env
├── .gitignore
├── docker-compose.yml
├── Dockerfile
├── pyrightconfig.json
├── README.md
├── backend/
│   ├── README.md
│   ├── pyproject.toml
│   ├── poetry.lock
│   ├── requirements.txt
│   ├── books.db
│   ├── test_hash.py
│   ├── app/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── schemas.py
│   │   ├── Repository/
│   │   │   ├── books.py
│   │   │   └── users.py
│   │   ├── dependencies/
│   │   │   ├── auth_dependencies.py
│   │   │   └── security.py
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   └── books.py
│   │   ├── services/
│   │   │   ├── ai.py
│   │   │   ├── ai_prompts.py
│   │   │   ├── auth.py
│   │   │   ├── auth_service.py
│   │   │   └── books.py
│   │   └── utils/
│   │       ├── groq_client.py
│   │       └── wrappers.py
│   └── tests/
│       ├── __init__.py
│       ├── test_auths.py
│       └── test_books.py
└── frontend/
	└── ui/
		├── assets/
		│   ├── ai-books.svg
		│   └── bookstore-hero.svg
		├── css/
		│   └── styles.css
		├── js/
		│   ├── auth.js
		│   ├── common.js
		│   ├── dashboard.js
		│   ├── profile.js
		│   ├── books-write.js
		│   ├── books-view.js
		│   ├── books-search.js
		│   ├── books-ai-search.js
		│   ├── books-ai-summary.js
		│   └── books-ai-recommendations.js
		└── pages/
			├── landing.html
			├── login.html
			├── register.html
			├── dashboard.html
			├── profile.html
			├── books-write.html
			├── books-view.html
			├── books-search.html
			├── books-ai-search.html
			├── books-ai-summary.html
			└── books-ai-recommendations.html
```

## Run Locally (Poetry)

```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload
```

## Run With Docker

From repository root:

```bash
docker compose up --build
```

## URLs

- API root: `http://127.0.0.1:8000/`
- UI landing: `http://127.0.0.1:8000/ui`
- Dashboard: `http://127.0.0.1:8000/ui/dashboard`
- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Frontend Routes

- `/ui`
- `/ui/login`
- `/ui/register`
- `/ui/dashboard`
- `/ui/profile`
- `/ui/books/write`
- `/ui/books/view`
- `/ui/books/search`
- `/ui/books/ai-search`
- `/ui/books/ai-summary`
- `/ui/books/ai-recommendations`

## Backend Docs

Detailed API/service notes are available in `backend/README.md`.
