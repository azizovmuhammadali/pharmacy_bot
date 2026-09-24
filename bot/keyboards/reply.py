from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from bot import texts as T

CATALOG = T.BTN_CATALOG
SEARCH = T.BTN_SEARCH
CART = T.BTN_CART
NEAREST_BRANCH = T.BTN_NEAREST_BRANCH


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text=CATALOG),
                KeyboardButton(text=SEARCH),
            ],
            [
                KeyboardButton(text=CART),
                KeyboardButton(text=NEAREST_BRANCH, request_location=True),
            ],
        ],
        resize_keyboard=True,
    )


def contact_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text=T.BTN_SEND_CONTACT,
                    request_contact=True,
                )
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
