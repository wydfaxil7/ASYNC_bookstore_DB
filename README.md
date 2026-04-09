# ASYNC Bookstore DB

Async FastAPI bookstore API + modular frontend UI.

Now includes BookGPT chatbot support with database-grounded responses.
Now includes cart management, inventory-aware stock handling, and storefront pages.

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
│   │   │   ├── carts.py
│   │   │   └── users.py
│   │   ├── dependencies/
│   │   │   ├── auth_dependencies.py
│   │   │   └── security.py
│   │   ├── routers/
│   │   │   ├── auth.py
│   │   │   ├── books.py
│   │   │   ├── carts.py
│   │   │   └── chat.py
│   │   ├── services/
│   │   │   ├── ai.py
│   │   │   ├── ai_prompts.py
│   │   │   ├── auth.py
│   │   │   ├── auth_service.py
│   │   │   ├── books.py
│   │   │   ├── carts.py
│   │   │   └── chatbot.py
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
		│   ├── cart-ui.js
		│   ├── chatbot.js
		│   ├── common.js
		│   ├── dashboard.js
		│   ├── profile.js
		│   ├── books-write.js
		│   ├── books-view.js
		│   ├── books-search.js
		│   ├── books-ai-search.js
		│   ├── books-ai-summary.js
		│   ├── books-ai-recommendations.js
		│   ├── product.js
		│   └── shop.js
		└── pages/
			├── product.html
			├── shop.html
			├── chatbot.html
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
- BookGPT UI: `http://127.0.0.1:8000/ui/chatbot`
- Shop UI: `http://127.0.0.1:8000/ui/shop`
- Product UI: `http://127.0.0.1:8000/ui/product?id=1`
- Chat API: `http://127.0.0.1:8000/chat`
- Cart API base: `http://127.0.0.1:8000/carts`
- Swagger: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Frontend Routes

- `/ui`
- `/ui/login`
- `/ui/register`
- `/ui/dashboard`
- `/ui/chatbot`
- `/ui/shop`
- `/ui/product?id={book_id}`
- `/ui/profile`
- `/ui/books/write`
- `/ui/books/view`
- `/ui/books/search`
- `/ui/books/ai-search`
- `/ui/books/ai-summary`
- `/ui/books/ai-recommendations`

## Backend Docs

Detailed API/service notes are available in `backend/README.md`.

## BookGPT Chatbot

- Endpoint: `POST /chat`
- Auth: protected route (Bearer JWT required)
- Grounding: checks real bookstore catalog before LLM response generation
- Supports:
	- exact store count queries
	- direct book-id lookup
	- fuzzy catalog search for typo-tolerant user input
- Response includes diagnostics such as `lookup_mode`, `matched_books_count`, and `store_book_count`.

## Cart And Inventory

- Cart endpoints are available under `/carts`.
- Supports add, get, update quantity, delete item, and clear cart actions.
- Stock is inventory-aware and updates as cart quantities change.
- Storefront includes quick-add modals, quantity steppers, and checkout-cart prompts.
