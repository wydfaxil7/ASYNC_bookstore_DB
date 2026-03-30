# 🛍️ ASYNC Bookstore API with AI-Powered Features

> A high-performance asynchronous Bookstore API built with **FastAPI, Async SQLAlchemy, PostgreSQL, and Groq AI**.

Designed with a **clean layered architecture** to ensure scalability, maintainability, and production-readiness. Now featuring **AI-powered book search, recommendations, and summaries**.

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
  - Filter by **published date range**
- 📦 Bulk book creation endpoint
- 🤖 **AI-Powered Features:**
  - **AI Book Search** - Natural language book discovery
  - **AI Recommendations** - Personalized book suggestions
  - **AI Summaries** - Story-like book summaries using Groq AI
- 🧠 Pydantic v2 schemas (`model_dump`, `from_attributes`)
- 🛡️ Centralized error handling using wrappers
- 📘 Auto-generated API docs (Swagger & ReDoc)  

---

## 📁 Project Structure

```bash
BOOKSTORE_DB/
├── app/
│   ├── Repository/
│   │   └── books.py
│   ├── services/
│   │   ├── books.py
│   │   ├── ai.py          # NEW: AI service functions
│   │   └── ai_prompts.py  # NEW: AI prompt templates
│   ├── routers/
│   │   └── books.py
│   ├── utils/
│   │   ├── wrappers.py
│   │   └── groq_client.py # NEW: Groq AI client
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── main.py
├── tests/
├── .env
├── pyproject.toml
└── README.md
```

---
## 📦 Tech Stack

| Tech            | Usage |
|-----------------|------|
| FastAPI         | Async web framework |
| SQLAlchemy      | Async ORM |
| PostgreSQL      | Database |
| **Groq AI**     | **AI-powered features (search, recommendations, summaries)** |
| Pydantic v2     | Validation & serialization |
| Poetry          | Dependency management |
| pytest + httpx  | Testing |

---

# 🛠️ Getting Started

## 📥 Clone Repository

```bash
git clone https://github.com/your-username/BOOKSTORE_DB.git
cd BOOKSTORE_DB
```
## 📦 Install Dependencies
```bash
poetry install
poetry shell
```
---

## ⚙️ Environment Variables

### Create a .env file:
```bash
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/bookstore
GROQ_API_KEY=your_groq_api_key_here
```

### 🗄️ Create Database Tables
```bash
python create_tables.py
```

### 🚀 Run the API
```bash
poetry run uvicorn app.main:app --reload
```
---

## 🔗 Server 
```bash
http://127.0.0.1:8000
```
---

## 📘 API Documentation
```bash
📄 Swagger UI → http://127.0.0.1:8000/docs
📕 ReDoc → http://127.0.0.1:8000/redoc
```
---

## 📌 Endpoints

### 📚 Books

| Method | Endpoint              | Description                          |
|:------:|----------------------|--------------------------------------|
| POST   | `/books`             | Create a new book                    |
| POST   | `/books/bulk`        | Bulk create multiple books           |
| GET    | `/books`             | Get books (filtering & pagination)   |
| GET    | `/books/{id}`        | Get a single book by ID              |
| PUT    | `/books/{id}`        | Update a book                        |
| DELETE | `/books/{id}`        | Delete a book                        |

### 🤖 AI-Powered Features

| Method | Endpoint                    | Description                          |
|:------:|----------------------------|--------------------------------------|
| GET    | `/books/search`            | AI-powered book search by query      |
| GET    | `/books/recommend`         | AI-powered book recommendations      |
| GET    | `/books/summary/search`    | AI-generated book summaries (by ID or name) |

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
### Filter by Date Range
```bash
/books?start_date=2000-01-01&end_date=2020-01-01
```
### Combined Filters
```bash
/books?author=John&genre=Fiction&limit=5&offset=0
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
Generate engaging, story-like summaries of books:

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

## ⚡ Bulk Insert Example
```bash
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
Centralized using service wrappers
Consistent API responses

Handles:

❌ 404 Not Found
⚠️ 400 Bad Request
💥 500 Internal Errors

---

## 💡 Key Learnings
- Async FastAPI architecture
- SQLAlchemy async queries
- Clean backend layering
- Pagination & filtering patterns
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
- 🔃 Sorting (sort_by, order)
- 🔐 Authentication & authorization
- 🔍 Advanced full-text search
- 🐳 Docker support
- ⚙️ CI/CD pipeline
- 🤝 Contributions
---
## Contributions are welcome!

### Fork → Create branch → Commit → PR 🚀
---
# ⭐ Final Note

This project demonstrates a production-ready backend structure using modern async Python tools, now enhanced with **cutting-edge AI capabilities** for intelligent book discovery and content generation.

🚀 Built with passion using FastAPI & Groq AI

---
# BOOKS in DATABASE
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
