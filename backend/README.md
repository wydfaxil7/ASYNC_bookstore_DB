# 🛍️ ASYNC Bookstore API with AI-Powered Features & Docker

> A high-performance asynchronous Bookstore API built with **FastAPI, Async SQLAlchemy, PostgreSQL, JWT Auth, and Groq AI**, now fully Dockerized.

Designed with a **clean layered architecture** to ensure scalability, maintainability, and production-readiness. Features **AI-powered book search, recommendations, and story-like summaries**.

---

## 🚀 Features

- ⚡ Fully asynchronous FastAPI endpoints
- 🗄️ Async SQLAlchemy with PostgreSQL
- 🧱 Clean architecture (Router → Service → Repository)
- 📚 Full CRUD operations on books
- 📄 Pagination with total count (`limit`, `offset`)
- 🔍 Dynamic filtering:
  - Filter by **author**
  - Filter by **genre**
  - Filter by **published date range** (supports year, year-month, or full date)
- 🔀 **Advanced sorting** by name, author, published_date, or genre (asc/desc)
- 📦 Bulk book creation endpoint
- 🛡️ JWT authentication & admin-only protections
- 🤖 **AI-Powered Features:**
  - **AI Book Search** — Natural language book discovery
  - **AI Recommendations** — Personalized book suggestions
  - **AI Summaries** — Story-like book summaries using Groq AI
  - **BookGPT Chatbot** — Contextual chat grounded on real store data
- 🛒 **Cart Management:**
  - Add/update/delete/clear user cart items
  - Quantity-aware cart totals
  - Inventory-aware stock reservation and release
- 🧠 Pydantic v2 schemas (`model_dump`, `from_attributes`)
- 🛡️ Centralized error handling using wrappers
- 📘 Auto-generated API docs (Swagger & ReDoc)
- 🐳 Fully Dockerized (API + PostgreSQL)

---

## 📁 Project Structure

```bash
BOOKSTORE_DB/
├── app/
│   ├── Repository/
│   │   ├── books.py
│   │   └── carts.py
│   ├── services/
│   │   ├── books.py
│   │   ├── ai.py          # AI service functions
│   │   ├── ai_prompts.py  # AI prompt templates
│   │   ├── chatbot.py     # BookGPT service logic
│   │   └── carts.py       # Cart service logic
│   ├── routers/
│   │   ├── books.py
│   │   ├── carts.py
│   │   └── chat.py
│   ├── utils/
│   │   ├── wrappers.py
│   │   └── groq_client.py # Groq AI client
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── main.py
├── tests/
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── pyproject.toml
└── README.md
```

---

## 📦 Tech Stack

| Tech            | Usage |
|-----------------|-------|
| FastAPI         | Async web framework |
| SQLAlchemy      | Async ORM |
| PostgreSQL      | Database |
| **Groq AI**     | **AI-powered features (search, recommendations, summaries)** |
| Pydantic v2     | Validation & serialization |
| Poetry          | Dependency management |
| pytest + httpx  | Testing |

---

## 🛠️ Getting Started

### 📥 Clone Repository

```bash
git clone https://github.com/your-username/BOOKSTORE_DB.git
cd BOOKSTORE_DB
```

### 📦 Install Dependencies

```bash
poetry install
poetry shell
```

---

## ⚙️ Environment Variables

Create a `.env` file:

```bash
DATABASE_URL=postgresql+asyncpg://wydfaxil:Aprinov-1428@localhost:5433/bookstore
GROQ_API_KEY=your_groq_api_key
SECRET_KEY=your_jwt_secret
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=7
```

> ⚠️ Use `localhost:5433` for local Python runs.  
> ⚠️ For Docker Compose, the `DATABASE_URL` should use `postgres:5432`.

---

### 🗄️ Create Database Tables

```bash
python create_tables.py
```

### 🚀 Run the API

**Local:**
```bash
poetry run uvicorn app.main:app --reload
```

**Dockerized:**
```bash
docker compose up --build
```

- FastAPI → host port `8000`
- PostgreSQL → host port `5433`

---

## 🔗 Server

```
http://127.0.0.1:8000
```

---

## 📘 API Documentation

```
📄 Swagger UI → http://127.0.0.1:8000/docs
📕 ReDoc      → http://127.0.0.1:8000/redoc
```

---

## 📌 Endpoints

### 📚 Books

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

### 🛒 Cart

| Method | Endpoint                | Description                                |
|:------:|-------------------------|--------------------------------------------|
| POST   | `/carts/add`            | Add a book to cart                         |
| GET    | `/carts`                | Get current user's cart                    |
| PUT    | `/carts/update/{id}`    | Update item quantity                       |
| DELETE | `/carts/delete/{id}`    | Delete an item from cart                   |
| DELETE | `/carts/clear`          | Clear all items in current user's cart     |

Notes:

- Cart operations are user-scoped via JWT auth.
- Cart totals include `total_items` and `total_price`.
- Book stock is adjusted on add/update/delete/clear cart operations.

---

## 🔍 Filtering & Pagination

### Pagination
```bash
/books?limit=10&offset=0
```

### Filter by Author
```bash
/books?author=Rowling
```

### Filter by Genre
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
- **Inventory-aware cart logic (reserve/release stock with quantity deltas)**
- **State consistency across cart add/update/delete/clear flows**
- **Auth-scoped customer operations for cart endpoints**
- **Schema evolution handling for existing DB tables (ALTER TABLE for new columns)**
- **Frontend/Backend contract design for diagnostics and totals (`lookup_mode`, `total_price`)**

---

## 🔮 Future Improvements

- ✅ **AI-Powered Search** (Implemented)
- ✅ **AI Recommendations** (Implemented)
- ✅ **AI Book Summaries** (Implemented)
- ✅ **Advanced Sorting** (Implemented)
- ✅ **Docker Support** (Implemented)
- ✅ **JWT Authentication & authorization** (Implemented)
- ✅ **BookGPT DB-grounded chat** (Implemented)
- ✅ **Cart API with inventory updates** (Implemented)
- 🔍 Advanced full-text search / trigram indexing
- 🧾 Order and checkout persistence (orders, order-items, payment states)
- 🧠 Recommendation personalization using user/cart history
- ⚙️ CI/CD pipeline with migration checks and integration tests
- 📈 Monitoring and structured logging dashboards

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