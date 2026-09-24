from aiogram import F, Router
from aiogram.types import Message

from bot import texts as T
from bot.keyboards.inline import product_list_kb
from bot.keyboards.reply import SEARCH
from bot.services import product as product_service
from bot.states import SearchStates

router = Router()


@router.message(F.text == SEARCH)
async def start_search(message: Message, state):
    await state.set_state(SearchStates.waiting_query)
    await message.answer(T.SEND_MEDICINE_NAME)


@router.message(SearchStates.waiting_query, F.text)
async def process_search(message: Message, state, session):
    await state.clear()

    query = message.text.strip()

    products = await product_service.search_products(
        session=session,
        query=query,
    )

    if not products:
        await message.answer(T.NO_PRODUCTS_FOUND)
        return

    await message.answer(
        text=T.SEARCH_RESULTS,
        reply_markup=product_list_kb(products),
    )
