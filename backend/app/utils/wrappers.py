#utils/wrappers.py
from functools import wraps
from fastapi import HTTPException
import logging
import traceback


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
            print("🔥 ERROR:", str(e))
            traceback.print_exc()   # 👈 VERY IMPORTANT
            raise HTTPException(status_code=500, detail=str(e))  # show actual error
    return wrapper