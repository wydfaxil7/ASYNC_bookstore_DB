# 🛍️ ASYNC Bookstore API

> A high-performance asynchronous Bookstore API built with **FastAPI, Async SQLAlchemy, and PostgreSQL**.

Designed with a **clean layered architecture** to ensure scalability, maintainability, and production-readiness.

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
- 🧠 Pydantic v2 schemas (`model_dump`, `from_attributes`)  
- 🛡️ Centralized error handling using wrappers  
- 📘 Auto-generated API docs (Swagger & ReDoc)  

---

## 📁 Project Structure

```bash
ASYNC_bookstore_DB/
├── app/
│   ├── Repository/
│   │   └── books.py
│   ├── services/
│   │   └── books.py
│   ├── routers/
│   │   └── books.py
│   ├── utils/
│   │   └── wrappers.py
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
| Pydantic v2     | Validation & serialization |
| Poetry          | Dependency management |
| pytest + httpx  | Testing |

---

# 🛠️ Getting Started

## 📥 Clone Repository

```bash
git clone https://github.com/wydfaxil7/ASYNC_bookstore_DB.git
cd ASYNC_bookstore_DB
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

### 📘 API Documentation
```bash
📄 Swagger UI → http://127.0.0.1:8000/docs
📕 ReDoc → http://127.0.0.1:8000/redoc
```
---

## 📌 Endpoints

### 📚 Books

| Method | Endpoint        | Description                          |
|:------:|----------------|--------------------------------------|
| POST   | `/books`       | Create a new book                    |
| POST   | `/books/bulk`  | Bulk create multiple books           |
| GET    | `/books`       | Get books (filtering & pagination)   |
| GET    | `/books/{id}`  | Get a single book by ID              |
| PUT    | `/books/{id}`  | Update a book                        |
| DELETE | `/books/{id}`  | Delete a book                        |

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

## ⚡ Bulk Insert Example
```bash
[
  {
    "name": "Atomic Habits",
    "author": "James Clear",
    "genre": "Self-help",
    "published_date": "2018-10-16",
    "description": "A guide to building good habits."
  }
]
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

---

## 🔮 Future Improvements
- 🔃 Sorting (sort_by, order)
- 🔐 Authentication & authorization
- 🔍 Full-text search
- 🐳 Docker support
- ⚙️ CI/CD pipeline
- 🤝 Contributions
---
## Contributions are welcome!

### Fork → Create branch → Commit → PR 🚀
---
# ⭐ Final Note

This project demonstrates a production-ready backend structure using modern async Python tools.

🚀 Built with passion using FastAPI

---

