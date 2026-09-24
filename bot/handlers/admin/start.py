from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, WebAppInfo
from aiogram.filters import CommandObject

from config import config

router = Router()

@router.message(Command("admin"))
async def cmd_admin(message: Message):
    # Faqat adminlarga ruxsat
    if message.from_user.id not in config.admin_ids:
        return
    
    # WebApp URL'iga ?tab=admin parametrini qo'shamiz
    web_app_url = f"{config.web_app_url}?tab=admin"
    
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="⚙️ Admin Panel", web_app=WebAppInfo(url=web_app_url))]],
        resize_keyboard=True
    )
    await message.answer("Admin panelni ochish uchun tugmani bosing:", reply_markup=kb)
