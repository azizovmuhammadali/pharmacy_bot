from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from bot.db.models import CartItem, Product


async def add_to_cart(
    session: AsyncSession,
    user_id: int,
    product_id: int,
    quantity: int = 1,
) -> bool:
    product = await session.get(Product, product_id)

    if not product or not product.is_active or product.stock <= 0:
        return False

    existing = await session.scalar(
        select(CartItem).where(
            CartItem.user_id == user_id,
            CartItem.product_id == product_id,
        )
    )

    if existing:
        existing.quantity = min(existing.quantity + quantity, product.stock)
    else:
        session.add(
            CartItem(
                user_id=user_id,
                product_id=product_id,
                quantity=min(quantity, product.stock),
            )
        )

    await session.commit()
    return True


async def get_cart_items(
    session: AsyncSession,
    user_id: int,
) -> list[CartItem]:
    result = await session.execute(
        select(CartItem)
        .where(CartItem.user_id == user_id)
        .options(selectinload(CartItem.product))
        .order_by(CartItem.id)
    )
    return list(result.scalars().all())


async def change_quantity(
    session: AsyncSession,
    item_id: int,
    user_id: int,
    delta: int,
) -> None:
    item = await session.get(CartItem, item_id)

    if not item or item.user_id != user_id:
        return

    product = await session.get(Product, item.product_id)

    if not product or not product.is_active:
        await session.delete(item)
        await session.commit()
        return

    new_quantity = item.quantity + delta

    if new_quantity <= 0 or product.stock <= 0:
        await session.delete(item)
    else:
        item.quantity = min(new_quantity, product.stock)

    await session.commit()


async def remove_item(
    session: AsyncSession,
    item_id: int,
    user_id: int,
) -> None:
    item = await session.get(CartItem, item_id)

    if not item or item.user_id != user_id:
        return

    await session.delete(item)
    await session.commit()


async def clear_cart(
    session: AsyncSession,
    user_id: int,
) -> None:
    await session.execute(
        delete(CartItem).where(CartItem.user_id == user_id)
    )
    await session.commit()
