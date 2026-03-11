# 🛍️ ASYNC Bookstore API

A **high‑performance asynchronous CRUD API** for managing books, built with **FastAPI**, **SQLAlchemy (async)**, and **SQLite** (or any SQL database).  
Designed for clean structure, professional routing & services, and full API documentation.

---

## 🚀 Features

✔ Asynchronous FastAPI endpoints for superior performance  
✔ Async SQLAlchemy database access  
✔ Full CRUD operations on books  
✔ Automatic interactive API documentation (`/docs`)  
✔ Clear separation of routers, services, repositories & utils  
✔ Easy to extend, test, and deploy  

---

## 📁 Project Structure
ASYNC_bookstore_DB/
├── app/
│   ├── Repository/
│   │   └── books.py                # Database operations
│   ├── services/
│   │   └── books.py                # Business logic
│   ├── routers/
│   │   └── books.py                # API routes
│   ├── utils/
│   │   └── wrappers.py             # Function wrappers for error handling
│   ├── database.py                 # Database connection
│   ├── main.py
│   ├── models.py                   # SQLAlchemy models
│   └── schemas.py                  # Pydantic schemas
├── books.db                        # SQLite database file
├── tests/                          # Test suite (pytest + httpx)
│   └── test_books.py
├── .env                            # Environment variables
├── .gitignore                      # Ignored files
├── pyproject.toml                  # Poetry config
└── README.md                        # Project overview (this file)

---

## 📦 Tech Stack

| Tool | Purpose |
|------|---------|
| **FastAPI** | Web framework for async APIs |
| **SQLAlchemy** | ORM for working with SQL databases |
| **SQLite** | Lightweight SQL database (default) |
| **Poetry** | Dependency & environment management |
| **Pydantic** | Data validation & serialization |
| **pytest + httpx** | Testing framework & async http client |

---

## 🛠️ Getting Started

### 💻 Requirements

- Python **3.10+**
- Yarn/Poetry for dependency management

---

### 📥 🏁 Setup

1. **Clone the repository**

```bash
git clone https://github.com/wydfaxil7/ASYNC_bookstore_DB.git
cd ASYNC_bookstore_DB
```
2. **Install dependencies with Poetry**

```Bash
poetry install
```

3. **Activate virtual environment**

```Bash
poetry shell
```

4. Create database tables

This will populate your books.db SQLite file:

```Bash
python create_tables.py
```

🚀 Run the API

Start the FastAPI server:

```Bash
uvicorn app.main:app --reload
```

The server will run at:

http://127.0.0.1:8000

📘 API Documentation

FastAPI auto‑generates interactive docs:

Swagger UI:
http://127.0.0.1:8000/docs

ReDoc:
http://127.0.0.1:8000/redoc

These UIs let you explore and test all endpoints easily.

📌 Available Endpoints
Method         Path	              Description
POST	        /books	           Create a new book
GET	          /books	           Get all books
GET         	/books/{id}      	 Get a single book
PUT         	/books/{id}	       Update a book
DELETE	      /books/{id}	       Delete a book

🧪 Tests

Tests use pytest, pytest‑asyncio, and httpx for async testing.

Run tests with:

```Bash
python -m pytest -v
```
Or simply:
```Bash
pytest -v
```
🧩 Error Handling

This project uses function wrappers to catch errors centrally and return consistent HTTP error responses.
Errors like 404 (not found) or unexpected server errors will be formatted by these wrappers.

⭐ Contributions

Contributions are welcome! Feel free to add features, documentation, or test improvements.

Fork the repository

Create a new branch (feature/your-feature)

Commit your changes

Open a pull request



*Thanks for checking out ASYNC Bookstore API!* 🚀
