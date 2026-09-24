import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher

from bot.db.base import async_session_factory, init_db
from bot.db.seed import seed_defaults
from bot.handlers import routers
from bot.middlewares.db import DBSessionMiddleware
from config import config


async def main() -> None:
    logging.basicConfig(level=logging.INFO)

    if not config.bot_token:
        sys.exit("BOT_TOKEN is missing in .env")

    await init_db()
    await seed_defaults()

    bot = Bot(token=config.bot_token)
    dp = Dispatcher()

    db_middleware = DBSessionMiddleware(async_session_factory)

    dp.message.middleware(db_middleware)
    dp.callback_query.middleware(db_middleware)

    dp.include_routers(*routers)

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        pass
