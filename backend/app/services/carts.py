from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.Repository import carts as repo
from app.Repository import books as books_repo
from app.schemas import (
    CartItemCreate,
    CartItemUpdate,
    CartItemRead,
    CartListResponse
)
from app.utils.wrappers import serv_wrapper

@serv_wrapper
async def add_to_cart_service(
    db: AsyncSession,
    user_id: int,
    payload: CartItemCreate
) -> CartListResponse:
    """
    Add item to cart
    id item is already in the cart, it increments
    """

    book = await books_repo.get_book(db, payload.book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    await repo.add_item(db, user_id, payload)

    items = await repo.get_user_cart(db, user_id)
    totals = await repo.get_cart_total(db, user_id)
    data = [CartItemRead.model_validate(item) for item in items]
    total_items = sum(item.quantity for item in items)

    return CartListResponse(
        data = data, 
        total_items = totals["total_items"], 
        total_price = totals["total_price"],
        message = "Item added to cart"
    )

@serv_wrapper
async def get_cart_service(
    db: AsyncSession,
    user_id: int
) -> CartListResponse:
    """
    Fetch all cart items for current user.
    """
    
    items = await repo.get_user_cart(db, user_id)
    totals = await repo.get_cart_total(db, user_id)
    data = [CartItemRead.model_validate(item) for item in items]
    total_items = sum(item.quantity for item in items)

    return CartListResponse(
        data = data,
        total_items = totals["total_items"],
        total_price = totals["total_price"],
        message = "Cart fetched successfully" if data else "Cart is empty"
    )

@serv_wrapper
async def update_cart_item_service(
    db:AsyncSession,
    user_id: int,
    item_id: int,
    payload: CartItemUpdate
) -> CartListResponse:
    """
    Update cart item quanity
    """

    item = await repo.get_item(db, item_id, user_id)
    if not item:
        # Backward compatibility: treat path value as book_id when item_id is not found.
        item = await repo.get_item_by_book_id(db, item_id, user_id)
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    await repo.update_item(db, item.id, user_id, payload.quantity)

    items = await repo.get_user_cart(db, user_id)
    totals = await repo.get_cart_total(db, user_id)
    data = [CartItemRead.model_validate(item) for item in items]
    total_items = sum(item.quantity for item in items)

    return CartListResponse(
        data = data,
        total_items = totals["total_items"],
        total_price = totals["total_price"],
        message = "Cart item updated successfully"
    )

@serv_wrapper
async def  delete_cart_item_service(
    db: AsyncSession,
    user_id: int,
    item_id: int
) -> CartListResponse:
    """
    Delete a cart item
    """

    item = await repo.get_item(db, item_id, user_id)
    if not item:
        # Backward compatibility: treat path value as book_id when item_id is not found.
        item = await repo.get_item_by_book_id(db, item_id, user_id)
    if not item:
        raise HTTPException(status_code=404, detail="Cart item not found")

    await repo.delete_item(db, item.id, user_id)

    items = await repo.get_user_cart(db, user_id)
    totals = await repo.get_cart_total(db, user_id)
    data = [CartItemRead.model_validate(item) for item in items]
    total_items = sum(item.quantity for item in items)

    return CartListResponse(
        data = data,
        total_items = totals["total_items"],
        total_price = totals["total_price"],
        message = "Cart item deleted successfully"
    )

@serv_wrapper
async def clear_cart_service(
    db: AsyncSession,
    user_id: int
) -> CartListResponse:
    """
    Clear all items in user cart
    """
    await repo.clear_cart(db, user_id)

    return CartListResponse(
        data = [],
        total_items = 0,
        total_price = 0.0,
        message = "Cart cleared successfully"
    )
