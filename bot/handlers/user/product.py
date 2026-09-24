from aiogram import F, Router
from aiogram.types import CallbackQuery

from bot import texts as T
from bot.keyboards.callbacks import ProductCB
from bot.keyboards.inline import product_detail_kb
from bot.services import product as product_service

router = Router()


@router.callback_query(ProductCB.filter(F.action == "view"))
async def view_product(
    callback: CallbackQuery,
    callback_data: ProductCB,
    session,
):
    if callback_data.product_id is None:
        await callback.answer()
        return

    product = await product_service.get_product(
        session=session,
        product_id=callback_data.product_id,
    )

    if not product or not product.is_active:
        await callback.answer(T.PRODUCT_NOT_FOUND, show_alert=True)
        return

    text = (
        f"📦 {product.name}\n\n"
        f"💵 {T.PRODUCT_PRICE}: {product.price:.2f}\n"
        f"📦 {T.PRODUCT_STOCK}: {product.stock}\n\n"
        f"📄 {T.PRODUCT_DESCRIPTION}:\n{product.description or '-'}\n\n"
        f"🧪 {T.PRODUCT_COMPOSITION}:\n{product.composition or '-'}\n\n"
        f"ℹ️ {T.PRODUCT_USAGE}:\n{product.usage_instructions or '-'}"
    )

    if callback.message:
        await callback.message.edit_text(
            text=text,
            reply_markup=product_detail_kb(product),
        )

    await callback.answer()
