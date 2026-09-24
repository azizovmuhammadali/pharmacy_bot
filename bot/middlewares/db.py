from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from bot.db.base import async_session_factory


class DBSessionMiddleware(BaseMiddleware):
    def __init__(self, session_factory=async_session_factory):
        self.session_factory = session_factory

    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: dict[str, Any],
    ) -> Any:
        if isinstance(event, (Message, CallbackQuery)):
            async with self.session_factory() as session:
                data["session"] = session
                return await handler(event, data)

        return await handler(event, data)
