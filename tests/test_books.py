# tests/test_books.py

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

# Global variable to store book id across tests
test_book_id = None

@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/")
    print("Root endpoint response:", response.json())  # debug
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World, hope all are okay :)"}


@pytest.mark.asyncio
async def test_create_book():
    global test_book_id
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/books", json={
            "name": "Test Book",
            "author": "Fazil Naeem",
            "genre": "Education",
            "published_date": "2026-03-11",
            "description": "Testing wrapper"
        })
    print("Create book response:", response.json())  # debug
    assert response.status_code == 200
    data = response.json()
    test_book_id = data.get("id")
    assert test_book_id is not None


@pytest.mark.asyncio
async def test_get_books():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        try:
            response = await ac.get("/books")
            print("Get books response:", response.json())  # debug
            assert response.status_code == 200
        except Exception as e:
            print("Exception in test_get_books:", e)
            raise e


@pytest.mark.asyncio
async def test_get_single_book():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        try:
            response = await ac.get(f"/books/{test_book_id}")
            print("Get single book response:", response.json())  # debug
            assert response.status_code == 200
        except Exception as e:
            print("Exception in test_get_single_book:", e)
            raise e


@pytest.mark.asyncio
async def test_update_book():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        try:
            response = await ac.put(f"/books/{test_book_id}", json={
                "name": "Updated Book",
                "author": "Fazil Naeem",
                "genre": "Education",
                "published_date": "2026-03-11",
                "description": "Updated description"
            })
            print("Update book response:", response.json())  # debug
            assert response.status_code == 200
        except Exception as e:
            print("Exception in test_update_book:", e)
            raise e


@pytest.mark.asyncio
async def test_delete_book():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        try:
            response = await ac.delete(f"/books/{test_book_id}")
            print("Delete book response:", response.json())  # debug
            assert response.status_code == 200
        except Exception as e:
            print("Exception in test_delete_book:", e)
            raise e