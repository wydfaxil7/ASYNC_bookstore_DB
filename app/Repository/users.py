#app/Repository/users.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models import User
from typing import Optional

async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
    """
    Retrives a user by primary key ID
    """
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()

async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
    """
    Retrives a user by unique username 
    """
    result = await db.execute(select(User).where(User.username == username))
    return result.scalar_one_or_none()

async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """
    Retrives a user by unique email
    """
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, username: str, email: str, hashed_password: str, is_admin: bool = False) -> User:
    """
    Creates and persists a new user record
    """ 
    db_user = User(
        username = username, 
        email = email,
        hashed_password = hashed_password,
        is_active = True,
        is_admin = is_admin
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user