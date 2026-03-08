# Async Bookstore API

This repository contains an **asynchronous CRUD API** for a bookstore built with **FastAPI**, **SQLAlchemy**, and **SQLite (or any SQL database)**.  
The API uses **async/await** patterns for high performance, and includes automatic interactive documentation via **Swagger UI**.

---

## 🚀 Features

- ✅ FastAPI framework for high‑performance APIs  
- ✅ Async SQLAlchemy database access  
- ✅ CRUD (Create, Read, Update, Delete) for books  
- ✅ Interactive API documentation (`/docs`)  
- ✅ Professional project structure  
- 🛠 Ready to switch to PostgreSQL or other databases

---

## 🗂️ Project Structure
ASYNC_bookstore_DB/
├── app/
│ ├── database.py # Database connection and session
│ ├── models.py # SQLAlchemy models
│ ├── schemas.py # Pydantic schemas
│ └── routers/
│ └── books.py # Book CRUD routes
├── create_tables.py # Script to create DB tables
├── books.db # SQLite database (ignored on push if in .gitignore)
├── pyproject.toml # Poetry config
├── poetry.lock # Dependency lock file
└── .gitignore # Files to ignore (venv, DB files, etc.)


---

## 🧠 How It Works

This API handles **bookstore data** with the following endpoints:

| Method | URL | Description |
|--------|-----|-------------|
| POST | `/books` | Create a new book |
| GET | `/books` | Get list of all books |
| GET | `/books/{id}` | Get a single book |
| PUT | `/books/{id}` | Update a book |
| DELETE | `/books/{id}` | Delete a book |

Interactive Swagger docs available at:
http://127.0.0.1:8000/docs


---

## 📦 Installation

Make sure you have **Python 3.10+** installed.

1. Clone the repository:

```bash
git clone https://github.com/wydfaxil7/ASYNC_bookstore_DB.git
cd ASYNC_bookstore_DB

2.Install dependencies using Poetry:

poetry install
🛠 Set Up Database

Before running the app, create the tables:

poetry run python create_tables.py

Run the API Server
poetry run uvicorn app.main:app --reload

The server will start on:

http://127.0.0.1:8000
📘 API Documentation

Visit:

http://127.0.0.1:8000/docs

This provides an interactive UI to test all endpoints using Swagger.

🐍 Tech Stack

FastAPI — High‑performance web framework for Python

SQLAlchemy — Database ORM

SQLite — Lightweight SQL database (changeable to PostgreSQL)

Poetry — Dependency management

Pydantic — Data validation and serialization
