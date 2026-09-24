from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from bot.db.models import (
    CartItem,
    Order,
    OrderItem,
    OrderStatus,
)


async def create_order(
    session: AsyncSession,
    user_id: int,
    full_name: str,
    phone: str,
    delivery_method: str,
    address: str | None = None,
    branch_id: int | None = None,
) -> Order:
    result = await session.execute(
        select(CartItem)
        .where(CartItem.user_id == user_id)
        .options(selectinload(CartItem.product))
    )

    cart_items = list(result.scalars().all())

    if not cart_items:
        raise ValueError("Cart is empty")

    order = Order(
        user_id=user_id,
        full_name=full_name,
        phone=phone,
        delivery_method=delivery_method,
        address=address,
        branch_id=branch_id,
        status=OrderStatus.pending.value,
    )

    session.add(order)
    await session.flush()

    for cart_item in cart_items:
        product = cart_item.product

        if not product or not product.is_active:
            raise ValueError("One of cart products is unavailable")

        if product.stock < cart_item.quantity:
            raise ValueError(f"Insufficient stock for {product.name}")

        session.add(
            OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=cart_item.quantity,
                price=product.price,
            )
        )

        product.stock -= cart_item.quantity

    await session.execute(
        delete(CartItem).where(CartItem.user_id == user_id)
    )

    await session.commit()

    return order


async def get_all_orders(session: AsyncSession) -> list[Order]:
    result = await session.execute(
        select(Order)
        .options(
            selectinload(Order.items),
            selectinload(Order.user),
        )
        .order_by(Order.created_at.desc())
    )

    return list(result.scalars().all())


async def get_order(
    session: AsyncSession,
    order_id: int,
) -> Order | None:
    result = await session.execute(
        select(Order)
        .options(
            selectinload(Order.items).selectinload(OrderItem.product),
            selectinload(Order.user),
        )
        .where(Order.id == order_id)
    )

    return result.scalar_one_or_none()


async def update_order_status(
    session: AsyncSession,
    order_id: int,
    status: str,
) -> Order | None:
    if status not in OrderStatus.values():
        raise ValueError("Invalid order status")

    order = await session.get(Order, order_id)

    if not order:
        return None

    order.status = status
    await session.commit()

    return order
