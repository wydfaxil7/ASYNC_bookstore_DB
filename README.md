# ASYNC Bookstore DB

This repository is now organized into two top-level folders:

- `backend/` - FastAPI API, models, services, tests
- `frontend/` - Multi-page UI assets (pages, css, js, images)

## Structure

```text
BOOKSTORE_DB/
├── backend/
│   ├── app/
│   ├── tests/
│   ├── pyproject.toml
│   ├── poetry.lock
│   └── README.md
├── frontend/
│   └── ui/
│       ├── pages/
│       ├── css/
│       ├── js/
│       └── assets/
└── README.md
```

## Run Backend

From repository root:

```bash
cd backend
poetry install
poetry run uvicorn app.main:app --reload
```

Then open:

- API root: `http://127.0.0.1:8000/`
- UI landing: `http://127.0.0.1:8000/ui`
- Swagger: `http://127.0.0.1:8000/docs`

## Frontend Routes

- `/ui` - Landing page
- `/ui/login` - Login page
- `/ui/register` - Register page
- `/ui/dashboard` - Book operations + AI featured operations
- `/ui/profile` - Profile page (`/auth/me`)

## Detailed Backend Documentation

Full backend feature documentation is available in:

- `backend/README.md`
