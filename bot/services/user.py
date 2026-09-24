from aiogram.types import User as TelegramUser
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.models import User


async def get_or_create_user(
    session: AsyncSession,
    tg_user: TelegramUser,
) -> User:
    user = await session.get(User, tg_user.id)

    if user:
        return user

    user = User(
        id=tg_user.id,
        full_name=tg_user.full_name or "Unknown",
        username=tg_user.username,
    )

    session.add(user)
    await session.commit()

    return user
