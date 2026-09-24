from aiogram import F, Router
from aiogram.types import CallbackQuery, Message

from bot import texts as T
from bot.keyboards.callbacks import CheckoutCB
from bot.keyboards.inline import branch_list_kb, delivery_kb
from bot.keyboards.reply import contact_kb
from bot.services import branch as branch_service
from bot.services import cart as cart_service
from bot.services import order as order_service
from bot.states import CheckoutStates

router = Router()


async def finalize_order(
    message: Message,
    state,
    session,
    address: str | None = None,
    branch_id: int | None = None,
) -> None:
    data = await state.get_data()

    phone = data.get("phone")
    delivery_method = data.get("delivery")

    if not phone or not delivery_method:
        await message.answer(T.CHECKOUT_ERROR)
        await state.clear()
        return

    try:
        order = await order_service.create_order(
            session=session,
            user_id=message.from_user.id,
            full_name=message.from_user.full_name or "Unknown",
            phone=phone,
            delivery_method=delivery_method,
            address=address,
            branch_id=branch_id,
        )

        await state.clear()

        status_label = T.STATUS_LABELS.get(order.status, order.status)

        await message.answer(
            text=T.ORDER_SUCCESS.format(
                order_id=order.id,
                status=status_label,
            )
        )

    except ValueError as e:
        await message.answer(T.ORDER_ERROR.format(error=str(e)))


@router.callback_query(CheckoutCB.filter(F.action == "start"))
async def start_checkout(callback: CallbackQuery, session, state):
    items = await cart_service.get_cart_items(
        session=session,
        user_id=callback.from_user.id,
    )

    if not items:
        await callback.answer(T.CART_EMPTY_ALERT, show_alert=True)
        return

    await state.set_state(CheckoutStates.phone)

    if callback.message:
        await callback.message.answer(
            text=T.SEND_PHONE,
            reply_markup=contact_kb(),
        )

    await callback.answer()


async def proceed_to_delivery(message: Message, state, phone: str):
    await state.update_data(phone=phone)
    await state.set_state(CheckoutStates.delivery)

    await message.answer(
        text=T.CHOOSE_DELIVERY,
        reply_markup=delivery_kb(),
    )


@router.message(CheckoutStates.phone, F.contact)
async def process_contact(message: Message, state):
    await proceed_to_delivery(
        message=message,
        state=state,
        phone=message.contact.phone_number,
    )


@router.message(CheckoutStates.phone, F.text)
async def process_phone_text(message: Message, state):
    phone = message.text.strip().replace(" ", "")

    if len(phone) < 10:
        await message.answer(T.INVALID_PHONE)
        return

    await proceed_to_delivery(message=message, state=state, phone=phone)


@router.callback_query(
    CheckoutStates.delivery,
    CheckoutCB.filter(F.action == "delivery"),
)
async def choose_delivery_method(
    callback: CallbackQuery,
    callback_data: CheckoutCB,
    session,
    state,
):
    delivery_method = callback_data.delivery

    if delivery_method not in {"delivery", "pickup"}:
        await callback.answer()
        return

    await state.update_data(delivery=delivery_method)

    if delivery_method == "delivery":
        await state.set_state(CheckoutStates.address)

        if callback.message:
            await callback.message.answer(T.ENTER_ADDRESS)
    else:
        branches = await branch_service.get_branches(session)

        if not branches:
            await state.update_data(delivery="delivery")
            await state.set_state(CheckoutStates.address)

            if callback.message:
                await callback.message.answer(T.NO_BRANCHES_USE_ADDRESS)
        else:
            await state.set_state(CheckoutStates.branch)

            if callback.message:
                await callback.message.answer(
                    text=T.CHOOSE_BRANCH,
                    reply_markup=branch_list_kb(branches),
                )

    await callback.answer()


@router.message(CheckoutStates.address, F.text)
async def process_address(message: Message, state, session):
    await finalize_order(
        message=message,
        state=state,
        session=session,
        address=message.text.strip(),
    )


@router.callback_query(
    CheckoutStates.branch,
    CheckoutCB.filter(F.action == "branch"),
)
async def choose_branch(
    callback: CallbackQuery,
    callback_data: CheckoutCB,
    session,
    state,
):
    branch_id = callback_data.branch_id

    if branch_id is None:
        await callback.answer()
        return

    branch = await branch_service.get_branch(session, branch_id)

    address = None

    if branch:
        address = f"{branch.name}, {branch.address}"

    if callback.message:
        await finalize_order(
            message=callback.message,
            state=state,
            session=session,
            address=address,
            branch_id=branch_id,
        )

    await callback.answer()
