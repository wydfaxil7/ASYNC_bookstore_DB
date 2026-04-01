#app/services/auth.py
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from passlib.context import CryptContext
from jose import JWTError, jwt

SECRET_KEY = "your_very_secure_random_secret_key_here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """
    Hash a plain text password using bcrypt_sha256, truncating to 72 bytes automatically.
    """
    truncated = password[:72]  # bcrypt max is 72 bytes
    return pwd_context.hash(truncated)

def verify_password(plain_password:str, hashed_password:str) -> bool:
    """"
    Verif a plain text password against stored hash.

    Args:
        plain_password: Password provided by user during Login
        hashed_password: Password hash stored in database

    Returns:
        True if the passwords match, False otherwise
    """
    truncated = plain_password[:72]  # bcrypt max is 72 bytes
    return pwd_context.verify(truncated, hashed_password)

def create_access_token(data:Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token with claims and expiration

    Args:
        data: Dictionary of claims to encode in token (e.g., {user_id: 1, "username: Jose"})
        expires_delta: Custome expiration time. if None, use default ACCESS_TOKEN EXPIRE_MINUTES

    Returns:
        Encoded JWT token as string.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt

def decode_access_token(token:str) -> Dict[str, Any]:
    """
    Decode and validate a JWT access token.
    
    Args:
        token: JWT token string
    
    Returns:
        Dictionary of claims (user_id, username, is_admin, exp, etc.)

    Raises:
        JWTError: if token is invalid, expired, or has wrong signatures
    """

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise e

