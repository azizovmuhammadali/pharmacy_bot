from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from bot import texts as T
from bot.keyboards.callbacks import CategoryCB
from bot.keyboards.inline import category_list_kb, product_list_kb
from bot.keyboards.reply import CATALOG
from bot.services import product as product_service

router = Router()


@router.message(F.text == CATALOG)
async def show_catalog(message: Message, session):
    categories = await product_service.get_categories(session)

    if not categories:
        await message.answer(T.NO_CATEGORIES)
        return

    await message.answer(
        text=T.CHOOSE_CATEGORY,
        reply_markup=category_list_kb(categories),
    )


@router.callback_query(CategoryCB.filter(F.action == "list"))
async def callback_categories(callback: CallbackQuery, session):
    categories = await product_service.get_categories(session)

    if callback.message:
        await callback.message.edit_text(
            text=T.CHOOSE_CATEGORY,
            reply_markup=category_list_kb(categories),
        )

    await callback.answer()


@router.callback_query(CategoryCB.filter(F.action == "open"))
async def callback_category_products(
    callback: CallbackQuery,
    callback_data: CategoryCB,
    session,
):
    if callback_data.category_id is None:
        await callback.answer()
        return

    products = await product_service.get_products_by_category(
        session=session,
        category_id=callback_data.category_id,
    )

    if products:
        text = T.AVAILABLE_PRODUCTS
    else:
        text = T.NO_PRODUCTS_IN_CATEGORY

    markup = product_list_kb(
        products,
        category_id=callback_data.category_id,
    )

    if callback.message:
        await callback.message.edit_text(
            text=text,
            reply_markup=markup,
        )

    await callback.answer()
