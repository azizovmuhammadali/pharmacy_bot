from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot import texts as T
from bot.db.models import OrderStatus

from .callbacks import (
    AdminOrderCB,
    AdminProductCB,
    CartCB,
    CategoryCB,
    CheckoutCB,
    ProductCB,
)


def category_list_kb(categories) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for category in categories:
        builder.button(
            text=category.name,
            callback_data=CategoryCB(
                action="open",
                category_id=category.id,
            ).pack(),
        )

    builder.adjust(2)
    return builder.as_markup()


def product_list_kb(products, category_id: int | None = None) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for product in products:
        builder.button(
            text=f"{product.name} — {product.price:.2f}",
            callback_data=ProductCB(
                action="view",
                product_id=product.id,
                category_id=category_id,
            ).pack(),
        )

    builder.adjust(1)

    builder.button(
        text=T.BTN_BACK_CATEGORIES,
        callback_data=CategoryCB(action="list").pack(),
    )

    return builder.as_markup()


def product_detail_kb(product) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=T.BTN_ADD_TO_CART,
        callback_data=CartCB(
            action="add",
            product_id=product.id,
        ).pack(),
    )

    builder.button(
        text=T.BTN_BACK_CATALOG,
        callback_data=CategoryCB(action="list").pack(),
    )

    builder.adjust(1)

    return builder.as_markup()


def cart_kb(items) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []

    for item in items:
        rows.append(
            [
                InlineKeyboardButton(
                    text=f"{item.product.name} × {item.quantity}",
                    callback_data="noop",
                )
            ]
        )

        rows.append(
            [
                InlineKeyboardButton(
                    text="➖",
                    callback_data=CartCB(action="dec", item_id=item.id).pack(),
                ),
                InlineKeyboardButton(
                    text="➕",
                    callback_data=CartCB(action="inc", item_id=item.id).pack(),
                ),
                InlineKeyboardButton(
                    text="🗑",
                    callback_data=CartCB(action="remove", item_id=item.id).pack(),
                ),
            ]
        )

    rows.append(
        [
            InlineKeyboardButton(
                text=T.BTN_CHECKOUT,
                callback_data=CheckoutCB(action="start").pack(),
            )
        ]
    )

    rows.append(
        [
            InlineKeyboardButton(
                text=T.BTN_CONTINUE_SHOPPING,
                callback_data=CategoryCB(action="list").pack(),
            )
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=rows)


def delivery_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=T.DELIVERY_LABELS["delivery"],
                    callback_data=CheckoutCB(
                        action="delivery",
                        delivery="delivery",
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text=T.DELIVERY_LABELS["pickup"],
                    callback_data=CheckoutCB(
                        action="delivery",
                        delivery="pickup",
                    ).pack(),
                ),
            ]
        ]
    )


def branch_list_kb(branches) -> InlineKeyboardMarkup:
    rows: list[list[InlineKeyboardButton]] = []

    for branch in branches:
        rows.append(
            [
                InlineKeyboardButton(
                    text=f"{branch.name}: {branch.address}",
                    callback_data=CheckoutCB(
                        action="branch",
                        branch_id=branch.id,
                    ).pack(),
                )
            ]
        )

    return InlineKeyboardMarkup(inline_keyboard=rows)


def admin_menu_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    builder.button(
        text=T.ADMIN_ADD_PRODUCT,
        callback_data=AdminProductCB(action="new").pack(),
    )

    builder.button(
        text=T.ADMIN_PRODUCTS,
        callback_data=AdminProductCB(action="list").pack(),
    )

    builder.button(
        text=T.ADMIN_ORDERS,
        callback_data=AdminOrderCB(action="list").pack(),
    )

    builder.adjust(1)

    return builder.as_markup()


def admin_category_select_kb(categories) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for category in categories:
        builder.button(
            text=category.name,
            callback_data=CategoryCB(
                action="admin_select",
                category_id=category.id,
            ).pack(),
        )

    builder.adjust(2)

    return builder.as_markup()


def admin_products_kb(products) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for product in products:
        status_icon = "✅" if product.is_active else "❌"
        builder.button(
            text=f"{status_icon} {product.name} | ombor: {product.stock}",
            callback_data=AdminProductCB(
                action="view",
                product_id=product.id,
            ).pack(),
        )

    builder.adjust(1)

    builder.button(
        text=T.ADMIN_ADD_PRODUCT,
        callback_data=AdminProductCB(action="new").pack(),
    )

    builder.button(
        text=T.BTN_BACK_ADMIN,
        callback_data=AdminProductCB(action="menu").pack(),
    )

    return builder.as_markup()


def admin_product_kb(product) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for field, label in T.FIELD_LABELS.items():
        builder.button(
            text=f"Tahrirlash: {label}",
            callback_data=AdminProductCB(
                action="edit",
                product_id=product.id,
                field=field,
            ).pack(),
        )

    builder.button(
        text=T.BTN_DEACTIVATE,
        callback_data=AdminProductCB(
            action="delete",
            product_id=product.id,
        ).pack(),
    )

    builder.button(
        text=T.BTN_BACK_PRODUCTS,
        callback_data=AdminProductCB(action="list").pack(),
    )

    builder.adjust(2)

    return builder.as_markup()


def admin_orders_kb(orders) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for order in orders:
        status_label = T.STATUS_LABELS.get(order.status, order.status)
        builder.button(
            text=f"#{order.id} | {status_label}",
            callback_data=AdminOrderCB(
                action="view",
                order_id=order.id,
            ).pack(),
        )

    builder.adjust(1)

    builder.button(
        text=T.BTN_BACK_ADMIN,
        callback_data=AdminOrderCB(action="menu").pack(),
    )

    return builder.as_markup()


def admin_order_detail_kb(order) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for status in OrderStatus:
        label = T.STATUS_LABELS.get(status.value, status.value)

        if order.status == status.value:
            label = f"👉 {label}"

        builder.button(
            text=label,
            callback_data=AdminOrderCB(
                action="status",
                order_id=order.id,
                status=status.value,
            ).pack(),
        )

    builder.adjust(2)

    builder.button(
        text=T.BTN_BACK_ORDERS,
        callback_data=AdminOrderCB(action="list").pack(),
    )

    return builder.as_markup()
