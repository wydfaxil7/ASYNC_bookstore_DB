# tests/test_auth.py

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app
from app.services.auth import get_password_hash, verify_password, create_access_token, create_refresh_token, decode_access_token
from fastapi import HTTPException

# Store test user info
test_user = {
    "username": "testuser",
    "email": "testuser@example.com",
    "password": "TestPass123!"
}

admin_user = {
    "username": "adminuser",
    "email": "admin@example.com",
    "password": "AdminPass123!",
    "is_admin": True
}

@pytest.mark.asyncio
async def test_password_hashing():
    password = "MySecurePassword123!"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed) is True
    assert verify_password("wrongpass", hashed) is False


@pytest.mark.asyncio
async def test_jwt_tokens():
    payload = {"user_id": 1, "username": "test", "is_admin": True}

    access = create_access_token(payload)
    refresh = create_refresh_token(payload)

    decoded_access = decode_access_token(access)
    decoded_refresh = decode_access_token(refresh)

    assert decoded_access["user_id"] == 1
    assert decoded_access["type"] == "access"

    assert decoded_refresh["type"] == "refresh"


@pytest.mark.asyncio
async def test_require_admin_dependency():
    from app.dependencies.auth_dependencies import require_admin

    # Admin user
    admin_payload = {"user_id": 1, "username": "admin", "is_admin": True}
    result = await require_admin(admin_payload)
    assert result["is_admin"] is True

    # Non-admin user should raise 403
    user_payload = {"user_id": 2, "username": "user", "is_admin": False}
    with pytest.raises(HTTPException) as exc_info:
        await require_admin(user_payload)
    assert exc_info.value.status_code == 403


@pytest.mark.asyncio
async def test_login_endpoint():
    """
    Integration test for /auth/login endpoint.
    Requires the user to exist in DB already.
    """
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # First, register a test user
        await ac.post("/auth/register", json=test_user)

        # Login with username
        response = await ac.post("/auth/login", json={
            "username": test_user["username"],
            "password": test_user["password"]
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

        # Login with email
        response = await ac.post("/auth/login", json={
            "email": test_user["email"],
            "password": test_user["password"]
        })
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data

        # Wrong password
        response = await ac.post("/auth/login", json={
            "username": test_user["username"],
            "password": "wrongpass"
        })
        assert response.status_code == 401