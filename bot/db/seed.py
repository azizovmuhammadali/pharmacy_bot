from sqlalchemy import func, select

from .base import async_session_factory
from .models import Branch, Category


async def seed_defaults() -> None:
    async with async_session_factory() as session:
        category_count = await session.scalar(
            select(func.count()).select_from(Category)
        )

        if category_count == 0:
            session.add_all(
                [
                    Category(name="Og'riq qoldiruvchilar"),
                    Category(name="Antibiotiklar"),
                    Category(name="Vitaminlar"),
                    Category(name="Shamollash va gripp"),
                    Category(name="Birinchi yordam"),
                    Category(name="Ovqat hazm qilish"),
                ]
            )

        branch_count = await session.scalar(
            select(func.count()).select_from(Branch)
        )

        if branch_count == 0:
            session.add_all(
                [
                    Branch(
                        name="Markaziy dorixona",
                        address="Asosiy ko'cha, 1-uy",
                        latitude=41.311516,
                        longitude=69.249514,
                        phone="+998900000001",
                    ),
                    Branch(
                        name="Shimoliy filial",
                        address="Shimoliy shohko'cha, 10-uy",
                        latitude=41.350000,
                        longitude=69.280000,
                        phone="+998900000002",
                    ),
                ]
            )

        await session.commit()
