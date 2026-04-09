#backend/app/Repository/carts.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload

from app.models import CartItem, Book
from app.schemas import CartItemCreate


async def add_item(
        db: AsyncSession, 
        user_id: int, 
        item_data: CartItemCreate
) -> CartItem:
    """
    Add item to cart or increment if exists.
    """
    book_result = await db.execute(
        select(Book).where(Book.id == item_data.book_id)
    )
    book = book_result.scalar_one_or_none()
    if not book:
        raise ValueError("Book not found")

    if book.stock < item_data.quantity:
        raise ValueError(f"Only {book.stock} pieces left")

    query = select(CartItem).where(
        (CartItem.user_id == user_id) &
        (CartItem.book_id == item_data.book_id)
    )
    result = await db.execute(query)
    existing = result.scalars().first()

    if existing:
        existing.quantity += item_data.quantity
        db.add(existing)
        book.stock -= item_data.quantity
        db.add(book)
        await db.commit()
        await db.refresh(existing)
        await db.refresh(book)
        return existing

    new_item = CartItem(
        user_id=user_id,
        book_id=item_data.book_id,
        quantity=item_data.quantity
    )
    db.add(new_item)
    book.stock -= item_data.quantity
    db.add(book)
    await db.commit()
    await db.refresh(new_item)
    await db.refresh(book)
    return new_item


async def get_user_cart(
        db: AsyncSession, 
        user_id: int
) -> list[CartItem]:
    """
    Get all cart items for a user, including book details.
    """
    query = (
        select(CartItem)
        .where(CartItem.user_id == user_id)
        .options(selectinload(CartItem.book))
        .order_by(CartItem.created_at.desc())
    )
    result = await db.execute(query)
    return result.scalars().all()


async def get_item(
        db: AsyncSession, 
        item_id: int, 
        user_id: int
) -> CartItem | None:
    """
    Get specific cart item and verify ownership.
    """
    query = select(CartItem).where(
        (CartItem.id == item_id) &
        (CartItem.user_id == user_id)
    )
    result = await db.execute(query)
    return result.scalars().first()


async def get_item_by_book_id(
        db: AsyncSession,
        book_id: int,
        user_id: int
) -> CartItem | None:
    """
    Get cart item by book id for a user.
    Useful when clients send book_id instead of cart item id.
    """
    query = select(CartItem).where(
        (CartItem.book_id == book_id) &
        (CartItem.user_id == user_id)
    )
    result = await db.execute(query)
    return result.scalars().first()


async def update_item(
    db: AsyncSession, 
    item_id: int, 
    user_id: int, 
    quantity: int
) -> CartItem:
    """
    Update quantity of cart item.
    """
    if quantity < 1:
        raise ValueError("Quantity must be at least 1")

    item = await get_item(db, item_id, user_id)
    if not item:
        raise ValueError("Cart item not found or unauthorized user")

    book_result = await db.execute(
        select(Book).where(Book.id == item.book_id)
    )
    book = book_result.scalar_one_or_none()
    if not book:
        raise ValueError("Book not found")

    quantity_delta = quantity - item.quantity
    if quantity_delta > 0 and book.stock < quantity_delta:
        raise ValueError(f"Only {book.stock} pieces left")

    book.stock -= quantity_delta
    item.quantity = quantity
    db.add(item)
    db.add(book)
    await db.commit()
    await db.refresh(item)
    await db.refresh(book)
    return item


async def delete_item(
        db: AsyncSession, 
        item_id: int, 
        user_id: int
) -> bool:
    """
    Delete item from cart.
    """
    item = await get_item(db, item_id, user_id)
    if not item:
        return False

    book_result = await db.execute(
        select(Book).where(Book.id == item.book_id)
    )
    book = book_result.scalar_one_or_none()
    if book:
        book.stock += item.quantity
        db.add(book)

    await db.delete(item)
    await db.commit()
    return True


async def clear_cart(db: AsyncSession, user_id: int) -> int:
    """
    Clear all items from user's cart.
    """
    items_result = await db.execute(
        select(CartItem).where(CartItem.user_id == user_id)
    )
    items = items_result.scalars().all()

    for item in items:
        book_result = await db.execute(
            select(Book).where(Book.id == item.book_id)
        )
        book = book_result.scalar_one_or_none()
        if book:
            book.stock += item.quantity
            db.add(book)

    query = delete(CartItem).where(CartItem.user_id == user_id)
    result = await db.execute(query)
    await db.commit()
    return result.rowcount


async def get_cart_total(
        db: AsyncSession, 
        user_id: int
) -> dict:
    """
    Get total items and total price for user cart.
    """
    items = await get_user_cart(db, user_id)

    total_items = sum(item.quantity for item in items)
    total_price = sum(item.quantity * float(item.book.price) for item in items if item.book)

    return {
        "total_items": total_items,
        "total_price": round(total_price, 2)
    }