from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton

from config import config

router = Router()

@router.message(Command("admin"))
async def cmd_admin(message: Message):
    # Faqat adminlarga ruxsat
    if message.from_user.id not in config.admin_ids:
        await message.answer("Bu buyruq faqat administratorlar uchun.")
        return
    
    # WebApp URL'iga ?tab=admin parametrini qo'shamiz
    web_app_url = f"{config.web_app_url}?tab=admin"
    
    kb = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="⚙️ Admin Panel", web_app=WebAppInfo(url=web_app_url))]],
        resize_keyboard=True
    )
    await message.answer("Admin panelni ochish uchun quyidagi tugmani bosing:", reply_markup=kb)
