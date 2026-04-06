# app/services/auth_service.py
from datetime import timedelta, timezone, datetime
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.services.auth import ACCESS_TOKEN_EXPIRE_MINUTES

from app.Repository.users import (
    get_user_by_email,
    get_user_by_username,
    create_user
)
from app.services.auth import (
    get_password_hash,
    verify_password,
    create_access_token
)

from app.schemas import UserCreate, UserLogin, UserRead, Token, TokenData
from app.models import User

async def register_user(db: AsyncSession, user_in: UserCreate) -> UserRead:
    """
    Registers a new user.
    - Validate username unique
    - Hash password safely
    - Persist user
    """
    if await get_user_by_username(db, user_in.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already exists"
        )
    
    if await get_user_by_email(db, user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists"
        )
    
    hashed = get_password_hash(user_in.password)  # truncated inside function
    user = await create_user(
        db,
        username=user_in.username,
        email=user_in.email,
        hashed_password=hashed
    )

    return UserRead.model_validate(user)

async def authenticate_user(db: AsyncSession, credentials: UserLogin) -> User:
    """
    Authenticates a user by email/username and password safely
    """
    user: Optional[User] = None

    if credentials.email:
        user = await get_user_by_email(db, credentials.email)
    elif credentials.username:
        user = await get_user_by_username(db, credentials.username)

    if not (credentials.email or credentials.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Must provide either email or username"
        )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    if not verify_password(credentials.password, user.hashed_password):  # truncated inside
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user"
        )
    
    return user

def create_user_access_token(user: User, expires_minutes: int = 60) -> Token:
    """
    Creates a JWT token for the authenticated user
    """
    expired = timedelta(minutes=expires_minutes)
    payload = {
        "user_id": user.id,
        "username": user.username,
        "is_admin": user.is_admin
    }

    token = create_access_token(payload, expires_delta=expired)
    return Token(access_token=token, token_type="bearer")

def make_token_data(user: User) -> TokenData:
    """
    Creates a TokenData object from a User model instance
    """
    return TokenData(
        user_id=user.id,
        username=user.username,
        is_admin=user.is_admin,
        exp=datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )