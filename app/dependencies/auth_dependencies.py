#app/dependencies/auth_dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from app.database import get_db
from app.services.auth import decode_access_token
from app.Repository.users import get_user_by_id
from app.models import User

# This tells FastAPI that the token will come from the Authorization header
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
bearer_scheme = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    """
    Decode JWT token from Authorization header and fetch the current user.
    Raises 401 if token is invalid or user not found.
    """
    token = credentials.credentials
    try:
        # Decode JWT and extract user_id
        payload = decode_access_token(token)
        return payload
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalaid Token"
        )
    #     user_id = payload.get("user_id")
    #     if not user_id:
    #         raise HTTPException(
    #             status_code=status.HTTP_401_UNAUTHORIZED,
    #             detail="Invalid token"
    #         )
    # except Exception:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Invalid token"
    #     )

    # # Fetch user from database
    # user = await get_user_by_id(user_id)
    # if not user:
    #     raise HTTPException(
    #         status_code=status.HTTP_404_NOT_FOUND,
    #         detail="User not found"
    #     )
    
    # return user

async def require_admin(current_user: dict = Depends(get_current_user)):
    """
    Dependency to ensure the current user has admin privileges.
    """

    if not current_user.get("is_admin", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    
    return current_user