import asyncio
import logging
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from bot.db.base import async_session_factory, init_db
from bot.db.seed import seed_defaults
from bot.handlers import routers
from bot.middlewares.db import DBSessionMiddleware
from config import config
from web.api import router as api_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pharmacy")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await seed_defaults()

    bot = Bot(token=config.bot_token)
    dp = Dispatcher()

    db_mw = DBSessionMiddleware(async_session_factory)
    dp.message.middleware(db_mw)
    dp.callback_query.middleware(db_mw)
    dp.include_routers(*routers)

    polling_task = asyncio.create_task(dp.start_polling(bot, handle_signals=False))
    app.state.bot = bot
    logger.info("Bot polling started inside web app")

    yield

    polling_task.cancel()
    try:
        await polling_task
    except asyncio.CancelledError:
        pass
    await bot.session.close()


app = FastAPI(title="Pharmacy Mini App", lifespan=lifespan)
app.include_router(api_router)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

import asyncio
import logging
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from bot.db.base import async_session_factory, init_db
from bot.db.seed import seed_defaults
from bot.handlers import routers
from bot.middlewares.db import DBSessionMiddleware
from config import config
from web.api import router as api_router

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pharmacy")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await seed_defaults()

    bot = Bot(token=config.bot_token)
    dp = Dispatcher()

    db_mw = DBSessionMiddleware(async_session_factory)
    dp.message.middleware(db_mw)
    dp.callback_query.middleware(db_mw)
    dp.include_routers(*routers)

    polling_task = asyncio.create_task(dp.start_polling(bot, handle_signals=False))
    app.state.bot = bot
    logger.info("Bot polling started inside web app")

    yield

    polling_task.cancel()
    try:
        await polling_task
    except asyncio.CancelledError:
        pass
    await bot.session.close()


app = FastAPI(title="Pharmacy Mini App", lifespan=lifespan)
app.include_router(api_router)
app.mount("/", StaticFiles(directory="static", html=True), name="static")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=False)

