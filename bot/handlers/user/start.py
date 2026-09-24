from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
    WebAppInfo,
)

from bot import texts as T
from bot.keyboards.reply import main_menu
from bot.services.user import get_or_create_user
from config import config

router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message, session):
    await get_or_create_user(session, message.from_user)

    await message.answer(text=T.WELCOME, reply_markup=main_menu())

    if config.web_app_url:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="📱 To'liq ilovani ochish",
                        web_app=WebAppInfo(url=config.web_app_url),
                    )
                ]
            ]
        )
        await message.answer(
            text="Yoki quyidagi tugma orqali chiroyli ilovani oching 👇",
            reply_markup=kb,
        )
