from decimal import Decimal

from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import CallbackQuery, Message

from bot import texts as T
from bot.keyboards.callbacks import CartCB
from bot.keyboards.inline import cart_kb
from bot.keyboards.reply import CART
from bot.services import cart as cart_service

router = Router()


async def render_cart(
    message: Message | None,
    session,
    user_id: int,
    edit: bool = False,
) -> None:
    if not message:
        return

    items = await cart_service.get_cart_items(session, user_id)

    if not items:
        text = T.CART_EMPTY
        markup = None
    else:
        lines: list[str] = []
        total = Decimal("0")

        for index, item in enumerate(items, start=1):
            line_total = item.product.price * item.quantity
            total += line_total

            lines.append(
                f"{index}. {item.product.name} × {item.quantity} "
                f"= {line_total:.2f}"
            )

        text = (
            f"{T.CART_TITLE}\n\n"
            + "\n".join(lines)
            + f"\n\n{T.CART_TOTAL}: {total:.2f}"
        )

        markup = cart_kb(items)

    if edit:
        try:
            await message.edit_text(text, reply_markup=markup)
        except TelegramBadRequest:
            await message.answer(text, reply_markup=markup)
    else:
        await message.answer(text, reply_markup=markup)


@router.message(F.text == CART)
async def open_cart(message: Message, session):
    await render_cart(message, session, message.from_user.id)


@router.callback_query(CartCB.filter(F.action == "open"))
async def callback_open_cart(callback: CallbackQuery, session):
    await render_cart(
        callback.message,
        session,
        callback.from_user.id,
        edit=True,
    )
    await callback.answer()


@router.callback_query(CartCB.filter(F.action == "add"))
async def callback_add_to_cart(
    callback: CallbackQuery,
    callback_data: CartCB,
    session,
):
    if callback_data.product_id is None:
        await callback.answer()
        return

    success = await cart_service.add_to_cart(
        session=session,
        user_id=callback.from_user.id,
        product_id=callback_data.product_id,
    )

    if success:
        await callback.answer(T.CART_ADDED)
    else:
        await callback.answer(T.CART_OUT_OF_STOCK, show_alert=True)


@router.callback_query(CartCB.filter(F.action == "inc"))
async def callback_increase_item(
    callback: CallbackQuery,
    callback_data: CartCB,
    session,
):
    if callback_data.item_id is not None:
        await cart_service.change_quantity(
            session=session,
            item_id=callback_data.item_id,
            user_id=callback.from_user.id,
            delta=1,
        )

    await render_cart(
        callback.message,
        session,
        callback.from_user.id,
        edit=True,
    )

    await callback.answer()


@router.callback_query(CartCB.filter(F.action == "dec"))
async def callback_decrease_item(
    callback: CallbackQuery,
    callback_data: CartCB,
    session,
):
    if callback_data.item_id is not None:
        await cart_service.change_quantity(
            session=session,
            item_id=callback_data.item_id,
            user_id=callback.from_user.id,
            delta=-1,
        )

    await render_cart(
        callback.message,
        session,
        callback.from_user.id,
        edit=True,
    )

    await callback.answer()


@router.callback_query(CartCB.filter(F.action == "remove"))
async def callback_remove_item(
    callback: CallbackQuery,
    callback_data: CartCB,
    session,
):
    if callback_data.item_id is not None:
        await cart_service.remove_item(
            session=session,
            item_id=callback_data.item_id,
            user_id=callback.from_user.id,
        )

    await render_cart(
        callback.message,
        session,
        callback.from_user.id,
        edit=True,
    )

    await callback.answer()


@router.callback_query(F.data == "noop")
async def callback_noop(callback: CallbackQuery):
    await callback.answer()
