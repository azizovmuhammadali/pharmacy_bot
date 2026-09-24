from aiogram.filters.callback_data import CallbackData


class CategoryCB(CallbackData, prefix="category"):
    action: str = "list"
    category_id: int | None = None


class ProductCB(CallbackData, prefix="product"):
    action: str = "view"
    product_id: int | None = None
    category_id: int | None = None


class CartCB(CallbackData, prefix="cart"):
    action: str = "open"
    item_id: int | None = None
    product_id: int | None = None


class CheckoutCB(CallbackData, prefix="checkout"):
    action: str = "start"
    delivery: str | None = None
    branch_id: int | None = None


class AdminProductCB(CallbackData, prefix="adm_prod"):
    action: str
    product_id: int | None = None
    field: str | None = None


class AdminOrderCB(CallbackData, prefix="adm_order"):
    action: str
    order_id: int | None = None
    status: str | None = None
