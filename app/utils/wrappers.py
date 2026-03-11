from functools import wraps
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

def serv_wrapper(func):
    """
    Decorator to wrap service function for centralized error handling
    """
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            raise HTTPException(status_code=500, detail="Internal Server ERROR!!")
    return wrapper