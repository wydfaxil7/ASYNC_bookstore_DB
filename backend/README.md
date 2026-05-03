# 📚 BOOKSTORE_DB — Async Bookstore Platform with AI Agent & Frontend

A production-grade async bookstore platform built with **FastAPI**, **PostgreSQL**, **Groq AI (Llama 3)**, and a fully custom **tool-calling AI agent engine** — now with a complete static frontend UI, Dockerized deployment, and a reusable local chatbot library.

---

## 🗂️ Project Structure

```
BOOKSTORE_DB/
├── backend/
│   ├── app/
│   │   ├── Repository/
│   │   │   ├── books.py            # DB queries — CRUD, search, filters, keywords
│   │   │   └── users.py            # DB queries — users
│   │   ├── dependencies/
│   │   │   ├── auth_dependencies.py  # require_admin, get_current_user guards
│   │   │   └── security.py           # Bearer scheme, token extraction
│   │   ├── routers/
│   │   │   ├── auth.py             # /auth/register, /auth/login, /auth/me
│   │   │   ├── books.py            # /books CRUD + AI search/recommend/summary
│   │   │   └── chat.py             # /chat — BookGPT tool-calling endpoint
│   │   ├── services/
│   │   │   ├── ai.py               # AI search, recommendations, summary orchestration
│   │   │   ├── ai_prompts.py       # Structured prompt builders for all AI features
│   │   │   ├── auth.py             # Auth helpers
│   │   │   ├── auth_service.py     # Registration, login, token logic
│   │   │   ├── books.py            # Book business logic
│   │   │   └── chatbot.py          # BookGPT: tool definitions, executor, per-user bots
│   │   ├── utils/
│   │   │   ├── groq_client.py      # Bridge to groq_chatbot_lib
│   │   │   └── wrappers.py         # Centralized error handling wrappers
│   │   ├── database.py             # Async engine and session factory
│   │   ├── main.py                 # App init, router registration, static UI mounting
│   │   ├── models.py               # SQLAlchemy models — Book, User
│   │   └── schemas.py              # Pydantic v2 request/response schemas
│   ├── tests/
│   │   ├── test_auths.py
│   │   └── test_books.py
│   ├── pyproject.toml
│   ├── requirements.txt
│   └── README.md
├── frontend/
│   └── ui/
│       ├── assets/
│       ├── css/
│       ├── js/
│       └── pages/
├── groq_chatbot_lib/               # Local reusable Python AI library
│   ├── groq_chatbot_lib/
│   │   ├── __init__.py             # Public exports
│   │   ├── client.py               # ChatbotClient — Groups 1, 2, 3
│   │   ├── tools.py                # Tool-calling engine — ToolDefinition, async loop
│   │   ├── extractor.py            # JSON extraction engine
│   │   └── utils.py                # Standalone helpers — Group 4
│   ├── tests/
│   ├── pyproject.toml
│   └── README.md
├── bookstore_backup.sql
├── docker-compose.yml
├── Dockerfile
└── README.md
```

---

## 🚀 Features

### ⚡ Core Backend
- Fully asynchronous end-to-end (FastAPI + Async SQLAlchemy + asyncpg)
- Clean **Router → Service → Repository** architecture
- JWT authentication with access and refresh tokens
- Role-based access control — admin-only write routes
- Full CRUD on books with bulk creation endpoint
- Pagination with total count (limit, offset)
- Dynamic filtering by author, genre, and date range (year / year-month / full date)
- Advanced sorting by name, author, published_date, or genre (asc/desc)
- Inventory-aware cart — stock reserved on add, released on delete/clear
- Pydantic v2 schemas (model_dump, from_attributes)
- Centralized error handling via service wrappers
- Auto-generated Swagger UI and ReDoc docs

### 🤖 AI-Powered Features
- 🔍 **AI Book Search** — natural language query → structured filters → DB lookup → keyword fallback
- 💡 **AI Recommendations** — multi-strategy fallback (primary genre → author → keywords → secondary genres)
- 📖 **AI Summaries** — story-style book summaries by ID or name via prompt engineering
- 💬 **BookGPT Chatbot** — DB-grounded tool-calling AI agent (see below)

### 💬 BookGPT — Tool-Calling AI Agent

The chat endpoint uses a **custom tool-calling loop** built from scratch inside `groq_chatbot_lib` — no LangChain:

1. 📨 User message + conversation history sent to Groq with four tool definitions
2. 🧠 LLM decides which tool(s) to call
3. 🗄️ Backend executes the tool against live PostgreSQL database
4. 📋 Tool results appended to history and sent back to the model
5. ✅ Model generates a final grounded reply

**Available tools:**
| Tool | Description |
|---|---|
| `search_books` | Full-text search by title, author, genre, or keyword |
| `get_book_by_id` | Fetch exact book by numeric ID |
| `count_books` | Return total catalog size |
| `get_recommendations` | Surface similar books |

Per-user bot instances maintained in memory with configurable memory limits — conversation history persists across turns within a session.

**Request example:**
```json
{
  "message": "do you have any books by Rowling?",
  "history_limit": 10
}
```

**Response fields:**
- `reply` — assistant response text
- `lookup_mode` — which logic path answered (search / exact_book_id / store_count / general_answer)
- `matched_books_count` — number of catalog matches used
- `store_book_count` — returned for count-oriented questions

### 🖥️ Frontend UI
Static HTML/CSS/JS pages served by FastAPI under `/ui`:

| Route | Page |
|---|---|
| `/ui` | Landing page |
| `/ui/login` | Login |
| `/ui/register` | Register |
| `/ui/dashboard` | User dashboard |
| `/ui/shop` | Browse catalog |
| `/ui/product?id={id}` | Book detail |
| `/ui/chatbot` | BookGPT chat UI |
| `/ui/books/ai-search` | AI search interface |
| `/ui/books/ai-summary` | Summary generator |
| `/ui/books/ai-recommendations` | Recommendations UI |
| `/ui/books/write` | Admin — create book |
| `/ui/books/edit` | Admin — edit book |

### 🐳 Docker
- Fully Dockerized (API + PostgreSQL)
- FastAPI → host port `8000`
- PostgreSQL → host port `5433`

---

## 🤖 groq_chatbot_lib

A general-purpose, reusable Python library for building Groq-powered AI chatbots and agents. Used internally by the backend but designed for any Python project.

### 📦 Install
```bash
pip install git+https://github.com/your-username/groq_chatbot_lib.git
```

### 🔧 Group 1 — Core Chat
```python
from groq_chatbot_lib import ChatbotClient

bot = ChatbotClient(api_key="...", model="llama-3.3-70b-versatile")
bot.set_system_prompt("You are a helpful assistant.")

reply = bot.ask("Hello!")           # stateful — adds to history
reply = bot.quick_ask("One-off")    # no memory effect
history = bot.get_history()
bot.reset()
```

### 🧠 Group 2 — Structured Output
```python
# Extract JSON dict
result = bot.ask_for_json("Return genre and mood as JSON")
# → {"genre": "fantasy", "mood": "dark"}

# Extract list of JSON objects
books = bot.ask_for_json_list("Return 3 books with title and author")
# → [{"title": "...", "author": "..."}, ...]

# Extract and validate required keys
data = bot.ask_with_schema(prompt, required_keys=["intent", "genre", "author"])
# → returns dict if all keys present, else None
```

### 🗂️ Group 3 — Memory & Context Control
```python
bot.set_memory_limit(10)            # auto-trim after every ask()
bot.inject_context("system", "User is browsing sci-fi.")
bot.trim_history(keep_last=4)
bot.get_recent_history(5)
bot.count_turns()
bot.has_system_prompt()
```

### 🛠️ Group 4 — Tool Calling (async)
```python
reply = await bot.ask_with_tools(
    user_message="Find books by Rowling",
    tools=BOOKSTORE_TOOLS,          # list[ToolDefinition]
    executor=my_async_executor      # async fn(ToolCall) -> ToolResult
)
```

**Defining tools:**
```python
from groq_chatbot_lib.tools import ToolDefinition, ToolParameter

search_tool = ToolDefinition(
    name="search_books",
    description="Search catalog by title, author, or genre.",
    parameters=[
        ToolParameter(name="query", type="string", description="Search term", required=False),
        ToolParameter(name="genre", type="string", description="Genre filter", required=False),
    ]
)
```

### 🧰 Standalone Utilities
```python
from groq_chatbot_lib import (
    format_history, history_to_text,
    count_tokens_estimate, is_within_token_limit, estimate_history_tokens,
    split_text_into_chunks,
    sanitize_message,
    extract_json, extract_json_list, validate_schema
)
```

---

## 📌 API Endpoints

### 🔐 Auth
| Method | Endpoint | Description |
|---|---|---|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login and get tokens |
| GET | `/auth/me` | Get current user |

### 📚 Books
| Method | Endpoint | Description |
|---|---|---|
| POST | `/books` | Create a book (admin only) |
| POST | `/books/bulk` | Bulk create books |
| GET | `/books` | Get books (filtering, sorting, pagination) |
| GET | `/books/{id}` | Get single book |
| PUT | `/books/{id}` | Update book (admin only) |
| DELETE | `/books/{id}` | Delete book (admin only) |

### 🤖 AI Features
| Method | Endpoint | Description |
|---|---|---|
| GET | `/books/ai-search` | Natural language book search |
| GET | `/books/recommendations` | AI-powered recommendations |
| GET | `/books/summary/search` | Story-style book summary |
| POST | `/chat` | BookGPT tool-calling chatbot |

### 🛒 Cart
| Method | Endpoint | Description |
|---|---|---|
| POST | `/carts/add` | Add book to cart |
| GET | `/carts` | Get current user's cart |
| PUT | `/carts/update/{id}` | Update item quantity |
| DELETE | `/carts/delete/{id}` | Remove item |
| DELETE | `/carts/clear` | Clear entire cart |

---

## 🔍 Filtering, Sorting & Pagination

```bash
# Pagination
/books?limit=10&offset=0

# Filter by author, genre
/books?author=Rowling&genre=Fantasy

# Filter by date range (year / year-month / full date)
/books?start_date=2000&end_date=2020
/books?start_date=2000-01&end_date=2020-12
/books?start_date=2000-01-01&end_date=2020-12-31

# Sorting
/books?sort_by=name&order=asc
/books?sort_by=published_date&order=desc

# Combined
/books?author=Rowling&genre=Fantasy&start_date=1997&end_date=2007&sort_by=name&order=asc&limit=5&offset=0
```

---

## 🛠️ Getting Started

### 📥 Clone Repository
```bash
git clone https://github.com/your-username/BOOKSTORE_DB.git
cd BOOKSTORE_DB
```

### 📦 Install Dependencies
```bash
cd backend
poetry install
poetry shell
```

### ⚙️ Environment Variables

Create `.env` in `backend/`:

```env
# Required
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5433/bookstore
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_jwt_secret

# Models
GROQ_CHAT_MODEL=llama-3.1-8b-instant
GROQ_SEARCH_MODEL=llama-3.1-8b-instant
GROQ_REQUEST_TIMEOUT_SECONDS=10

# AI timeouts
AI_SEARCH_TIMEOUT_SECONDS=5
AI_RECOMMENDATION_TIMEOUT_SECONDS=5
AI_SUMMARY_TIMEOUT_SECONDS=10

# Chat
CHAT_MEMORY_LIMIT=10
CHAT_CATALOG_SEARCH_LIMIT=5

# Auth
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7

# Prompt templates — use [[placeholder]] tokens to avoid Docker interpolation
GROQ_SYSTEM_PROMPT=...
BOOK_SEARCH_PROMPT_TEMPLATE=...
BOOK_RECOMMENDATION_PROMPT_TEMPLATE=...
BOOK_CHAT_PROMPT_TEMPLATE=...
BOOK_SUMMARY_PROMPT_TEMPLATE=...
```

> ⚠️ Use `localhost:5433` for local runs. For Docker Compose use `postgres:5432`.

### 🚀 Run Locally
```bash
poetry run uvicorn app.main:app --reload
```

Tables are created automatically on startup — no migration script needed.

### 🐳 Run with Docker
```bash
docker compose up --build
```

---

## 📘 API Documentation
- 📄 Swagger UI → `http://127.0.0.1:8000/docs`
- 📕 ReDoc → `http://127.0.0.1:8000/redoc`

---

## 🧪 Tests
```bash
cd backend
poetry run pytest -v
```

---

## 📦 Tech Stack

| Tech | Usage |
|---|---|
| **FastAPI** | Async web framework |
| **Async SQLAlchemy** | Async ORM |
| **PostgreSQL** | Primary database |
| **Groq AI (Llama 3)** | LLM for all AI features |
| **Pydantic v2** | Validation & serialization |
| **Poetry** | Dependency management |
| **pytest + httpx** | Testing |
| **Docker + Compose** | Containerization |
| **JWT (python-jose)** | Authentication |

---

## 🔮 Future Improvements
- 🔍 Advanced full-text search with trigram indexing
- 🧾 Order and checkout persistence (orders, order-items, payment states)
- 🧠 Recommendation personalization using user/cart history
- ⚙️ CI/CD pipeline with migration checks and integration tests
- 📈 Monitoring and structured logging dashboards
- 🌐 RAG pipeline with vector database for smarter catalog search

---

## ⭐ Final Note

This project demonstrates a production-ready backend structure using modern async Python, enhanced with a **custom-built AI agent tooling layer** for intelligent book discovery, grounded conversation, and content generation — built without relying on frameworks like LangChain.

🚀 Built with FastAPI & Groq AI
