from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.dependencies.auth_dependencies import get_current_user
from app.schemas import CartItemCreate, CartListResponse, CartItemUpdate
from app.services.carts import (
    add_to_cart_service,
    get_cart_service,
    update_cart_item_service,
    delete_cart_item_service,
    clear_cart_service
)

router = APIRouter(prefix="/carts", tags=["carts"])

@router.post("/add", response_model=CartListResponse)
async def add_to_cart(
    payload: CartItemCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db) 
):
    """
    Add item to cart, if item alread exists, it increments
    """

    return await add_to_cart_service(db, current_user["user_id"], payload)


@router.get("", response_model=CartListResponse)
async def get_cart(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Get all cart items for the current user.
    """
    return await get_cart_service(db, current_user["user_id"])


@router.put("/update/{item_id}", response_model=CartListResponse)
async def update_cart_item(
    item_id: int,
    payload: CartItemUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Update quantity of a single cart item
    """
    return await update_cart_item_service(db, current_user["user_id"], item_id, payload)


@router.delete("/delete/{item_id}", response_model=CartListResponse)
async def delete_cart_item(
    item_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a single cart item
    """
    return await delete_cart_item_service(db, current_user["user_id"], item_id)


@router.delete("/clear", response_model=CartListResponse)
async def clear_cart(
    db: AsyncSession = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """
    Clear all items from the cart
    """
    return await clear_cart_service(db, current_user["user_id"])