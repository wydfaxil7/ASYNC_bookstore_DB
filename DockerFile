FROM python:3.14-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    build-essential \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Add Poetry to PATH
ENV PATH="/root/.local/bin:$PATH"

# Copy groq_chatbot_lib first so it can be installed
COPY groq_chatbot_lib /app/groq_chatbot_lib

# Copy dependency files from backend for caching
COPY backend/pyproject.toml backend/poetry.lock /app/

# Install dependencies via Poetry
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Install groq_chatbot_lib as local package
RUN pip install /app/groq_chatbot_lib

# Copy runtime application and frontend assets
COPY backend/app /app/app
COPY frontend /app/frontend

# Expose fastapi port
EXPOSE 8000

# Run FastAPI
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]