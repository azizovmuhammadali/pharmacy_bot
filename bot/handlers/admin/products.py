from decimal import Decimal, InvalidOperation

from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message

from bot import texts as T
from bot.db.models import Product
from bot.filters import IsAdmin
from bot.keyboards.callbacks import AdminProductCB, CategoryCB
from bot.keyboards.inline import (
    admin_category_select_kb,
    admin_menu_kb,
    admin_product_kb,
    admin_products_kb,
)
from bot.services import product as product_service
from bot.states import AddProductStates, EditProductStates

router = Router()


@router.message(Command("admin"), IsAdmin())
async def admin_home(message: Message):
    await message.answer(
        text=T.ADMIN_PANEL,
        reply_markup=admin_menu_kb(),
    )


@router.callback_query(AdminProductCB.filter(F.action == "menu"), IsAdmin())
async def admin_menu(callback: CallbackQuery):
    if callback.message:
        await callback.message.edit_text(
            text=T.ADMIN_PANEL,
            reply_markup=admin_menu_kb(),
        )

    await callback.answer()


# ---- Create product ----

@router.callback_query(AdminProductCB.filter(F.action == "new"), IsAdmin())
async def product_new(callback: CallbackQuery, state):
    await state.set_state(AddProductStates.name)

    if callback.message:
        await callback.message.answer(T.SEND_PRODUCT_NAME)

    await callback.answer()


@router.message(AddProductStates.name, F.text, IsAdmin())
async def product_name(message: Message, state, session):
    await state.update_data(name=message.text.strip())

    categories = await product_service.get_categories(session)

    await state.set_state(AddProductStates.category)

    await message.answer(
        text=T.CHOOSE_CATEGORY,
        reply_markup=admin_category_select_kb(categories),
    )


@router.callback_query(
    AddProductStates.category,
    CategoryCB.filter(F.action == "admin_select"),
    IsAdmin(),
)
async def product_category(
    callback: CallbackQuery,
    callback_data: CategoryCB,
    state,
):
    if callback_data.category_id is None:
        await callback.answer()
        return

    await state.update_data(category_id=callback_data.category_id)
    await state.set_state(AddProductStates.price)

    if callback.message:
        await callback.message.answer(T.SEND_PRICE)

    await callback.answer()


@router.message(AddProductStates.price, F.text, IsAdmin())
async def product_price(message: Message, state):
    try:
        price = Decimal(message.text.replace(",", ".").strip())
    except InvalidOperation:
        await message.answer(T.INVALID_PRICE)
        return

    if price <= 0:
        await message.answer(T.PRICE_MUST_BE_POSITIVE)
        return

    await state.update_data(price=price)
    await state.set_state(AddProductStates.stock)

    await message.answer(T.SEND_STOCK)


@router.message(AddProductStates.stock, F.text, IsAdmin())
async def product_stock(message: Message, state):
    try:
        stock = int(message.text.strip())
    except ValueError:
        await message.answer(T.INVALID_STOCK)
        return

    if stock < 0:
        await message.answer(T.STOCK_NEGATIVE)
        return

    await state.update_data(stock=stock)
    await state.set_state(AddProductStates.description)

    await message.answer(T.SEND_DESCRIPTION)


@router.message(AddProductStates.description, F.text, IsAdmin())
async def product_description(message: Message, state):
    text = None if message.text.strip() == "-" else message.text.strip()

    await state.update_data(description=text)
    await state.set_state(AddProductStates.composition)

    await message.answer(T.SEND_COMPOSITION)


@router.message(AddProductStates.composition, F.text, IsAdmin())
async def product_composition(message: Message, state):
    text = None if message.text.strip() == "-" else message.text.strip()

    await state.update_data(composition=text)
    await state.set_state(AddProductStates.usage)

    await message.answer(T.SEND_USAGE)


@router.message(AddProductStates.usage, F.text, IsAdmin())
async def product_usage(message: Message, state, session):
    usage_instructions = (
        None if message.text.strip() == "-" else message.text.strip()
    )

    data = await state.get_data()

    product = Product(
        name=data["name"],
        category_id=data["category_id"],
        price=data["price"],
        stock=data["stock"],
        description=data.get("description"),
        composition=data.get("composition"),
        usage_instructions=usage_instructions,
    )

    session.add(product)
    await session.commit()

    await state.clear()

    await message.answer(
        text=T.PRODUCT_CREATED.format(product_id=product.id)
    )


# ---- Read products ----

@router.callback_query(AdminProductCB.filter(F.action == "list"), IsAdmin())
async def product_list(callback: CallbackQuery, session):
    products = await product_service.get_products(session)

    if callback.message:
        await callback.message.edit_text(
            text=T.PRODUCTS_LIST,
            reply_markup=admin_products_kb(products),
        )

    await callback.answer()


@router.callback_query(AdminProductCB.filter(F.action == "view"), IsAdmin())
async def product_view(
    callback: CallbackQuery,
    callback_data: AdminProductCB,
    session,
):
    if callback_data.product_id is None:
        await callback.answer()
        return

    product = await product_service.get_product(
        session=session,
        product_id=callback_data.product_id,
    )

    if not product:
        await callback.answer(T.PRODUCT_NOT_FOUND, show_alert=True)
        return

    active_label = "Ha" if product.is_active else "Yo'q"

    text = (
        f"ID: {product.id}\n"
        f"Nom: {product.name}\n"
        f"Narx: {product.price:.2f}\n"
        f"Ombor: {product.stock}\n"
        f"Faol: {active_label}\n\n"
        f"Tavsif:\n{product.description or '-'}\n\n"
        f"Tarkib:\n{product.composition or '-'}\n\n"
        f"Qo'llash:\n{product.usage_instructions or '-'}"
    )

    if callback.message:
        await callback.message.edit_text(
            text=text,
            reply_markup=admin_product_kb(product),
        )

    await callback.answer()


# ---- Update product ----

@router.callback_query(AdminProductCB.filter(F.action == "edit"), IsAdmin())
async def product_edit_start(
    callback: CallbackQuery,
    callback_data: AdminProductCB,
    state,
):
    if callback_data.product_id is None or callback_data.field is None:
        await callback.answer()
        return

    await state.set_state(EditProductStates.value)
    await state.update_data(
        product_id=callback_data.product_id,
        field=callback_data.field,
    )

    label = T.FIELD_LABELS.get(
        callback_data.field,
        callback_data.field,
    )

    if callback.message:
        await callback.message.answer(T.SEND_NEW_VALUE.format(label=label))

    await callback.answer()


@router.message(EditProductStates.value, F.text, IsAdmin())
async def product_edit_value(message: Message, state, session):
    data = await state.get_data()

    product_id = data.get("product_id")
    field = data.get("field")

    if not product_id or not field:
        await state.clear()
        await message.answer(T.EDIT_ERROR)
        return

    product = await product_service.get_product(session, product_id)

    if not product:
        await state.clear()
        await message.answer(T.PRODUCT_NOT_FOUND)
        return

    raw_value = message.text.strip()

    try:
        if field == "price":
            value = Decimal(raw_value.replace(",", "."))

            if value <= 0:
                raise ValueError

        elif field == "stock":
            value = int(raw_value)

            if value < 0:
                raise ValueError

        elif field == "name":
            if not raw_value:
                raise ValueError

            value = raw_value

        else:
            value = None if raw_value == "-" else raw_value

    except (InvalidOperation, ValueError):
        await message.answer(T.INVALID_VALUE)
        return

    setattr(product, field, value)

    await session.commit()
    await state.clear()

    await message.answer(T.PRODUCT_UPDATED)


# ---- Delete / deactivate product ----

@router.callback_query(AdminProductCB.filter(F.action == "delete"), IsAdmin())
async def product_delete(
    callback: CallbackQuery,
    callback_data: AdminProductCB,
    session,
):
    if callback_data.product_id is None:
        await callback.answer()
        return

    product = await product_service.get_product(
        session=session,
        product_id=callback_data.product_id,
    )

    if not product:
        await callback.answer(T.PRODUCT_NOT_FOUND, show_alert=True)
        return

    product.is_active = False
    product.stock = 0

    await session.commit()

    products = await product_service.get_products(session)

    if callback.message:
        await callback.message.edit_text(
            text=T.PRODUCTS_LIST,
            reply_markup=admin_products_kb(products),
        )

    await callback.answer(T.PRODUCT_DEACTIVATED)
