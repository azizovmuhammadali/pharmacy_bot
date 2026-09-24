from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot import texts as T
from bot.filters import IsAdmin
from bot.keyboards.callbacks import AdminOrderCB
from bot.keyboards.inline import (
    admin_menu_kb,
    admin_order_detail_kb,
    admin_orders_kb,
)
from bot.services import order as order_service

router = Router()


@router.message(Command("admin_orders"), IsAdmin())
async def orders_home(message: Message, session):
    orders = await order_service.get_all_orders(session)

    await message.answer(
        text=T.ORDERS_LIST,
        reply_markup=admin_orders_kb(orders),
    )


@router.callback_query(AdminOrderCB.filter(F.action == "list"), IsAdmin())
async def orders_list(callback: CallbackQuery, session):
    orders = await order_service.get_all_orders(session)

    if callback.message:
        await callback.message.edit_text(
            text=T.ORDERS_LIST,
            reply_markup=admin_orders_kb(orders),
        )

    await callback.answer()


@router.callback_query(AdminOrderCB.filter(F.action == "menu"), IsAdmin())
async def orders_menu(callback: CallbackQuery):
    if callback.message:
        await callback.message.edit_text(
            text=T.ADMIN_PANEL,
            reply_markup=admin_menu_kb(),
        )

    await callback.answer()


@router.callback_query(AdminOrderCB.filter(F.action == "view"), IsAdmin())
async def order_view(
    callback: CallbackQuery,
    callback_data: AdminOrderCB,
    session,
):
    if callback_data.order_id is None:
        await callback.answer()
        return

    order = await order_service.get_order(
        session=session,
        order_id=callback_data.order_id,
    )

    if not order:
        await callback.answer(T.ORDER_NOT_FOUND, show_alert=True)
        return

    status_label = T.STATUS_LABELS.get(order.status, order.status)
    delivery_label = T.DELIVERY_LABELS.get(
        order.delivery_method,
        order.delivery_method,
    )

    lines = [
        f"Buyurtma #{order.id}",
        f"Holat: {status_label}",
        f"Foydalanuvchi ID: {order.user_id}",
        f"Ism: {order.full_name}",
        f"Telefon: {order.phone}",
        f"Yetkazib berish: {delivery_label}",
        f"Manzil: {order.address or '-'}",
        "",
        "Mahsulotlar:",
    ]

    for item in order.items:
        product_name = (
            item.product.name if item.product else f"Product {item.product_id}"
        )

        lines.append(
            f"- {product_name} × {item.quantity} @ {item.price:.2f}"
        )

    if callback.message:
        await callback.message.edit_text(
            text="\n".join(lines),
            reply_markup=admin_order_detail_kb(order),
        )

    await callback.answer()


@router.callback_query(AdminOrderCB.filter(F.action == "status"), IsAdmin())
async def order_status_update(
    callback: CallbackQuery,
    callback_data: AdminOrderCB,
    session,
):
    if callback_data.order_id is None or callback_data.status is None:
        await callback.answer()
        return

    try:
        await order_service.update_order_status(
            session=session,
            order_id=callback_data.order_id,
            status=callback_data.status,
        )
    except ValueError:
        await callback.answer(T.INVALID_STATUS, show_alert=True)
        return

    order = await order_service.get_order(
        session=session,
        order_id=callback_data.order_id,
    )

    if order and callback.message:
        status_label = T.STATUS_LABELS.get(order.status, order.status)

        await callback.message.edit_text(
            text=T.ORDER_STATUS_UPDATED.format(
                order_id=order.id,
                status=status_label,
            ),
            reply_markup=admin_order_detail_kb(order),
        )

    await callback.answer(T.STATUS_UPDATED)
