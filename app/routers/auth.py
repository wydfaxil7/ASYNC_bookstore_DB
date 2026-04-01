#app/routers/auth.py
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas import UserCreate, UserRead, UserLogin, Token
from app.services.auth_service import(
    register_user,
    authenticate_user,
    create_user_access_token
)
from app.dependencies.auth_dependencies import get_current_user
from app.dependencies.security import get_current_user_from_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Register a new user

    - **user_data**: User registration data (username, email, password)
    """
    return await register_user(db, user_data)

@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, db: AsyncSession = Depends(get_db)):
    """
    Authenticate user and return JWT access token.

    - either **username/email** + **password**
    """
    user = await authenticate_user(db, credentials)
    token = create_user_access_token(user)
    return token

@router.get("/me")
async def get_me(current_user=Depends(get_current_user_from_token)):
    """
    Get details of the current user based on the JWT token provided in the Authorization header.
    """
    return current_user
