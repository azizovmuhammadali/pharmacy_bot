from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import Category, Product


async def get_categories(session: AsyncSession) -> list[Category]:
    result = await session.execute(
        select(Category).order_by(Category.name)
    )
    return list(result.scalars().all())


async def get_products_by_category(
    session: AsyncSession,
    category_id: int,
    limit: int = 50,
) -> list[Product]:
    result = await session.execute(
        select(Product)
        .where(
            Product.category_id == category_id,
            Product.is_active == True,
        )
        .order_by(Product.name)
        .limit(limit)
    )
    return list(result.scalars().all())


async def search_products(
    session: AsyncSession,
    query: str,
    limit: int = 50,
) -> list[Product]:
    result = await session.execute(
        select(Product)
        .where(
            Product.is_active == True,
            Product.name.ilike(f"%{query}%"),
        )
        .order_by(Product.name)
        .limit(limit)
    )
    return list(result.scalars().all())


async def get_product(
    session: AsyncSession,
    product_id: int,
) -> Product | None:
    return await session.get(Product, product_id)


async def get_products(session: AsyncSession) -> list[Product]:
    result = await session.execute(
        select(Product).order_by(Product.id.desc())
    )
    return list(result.scalars().all())
