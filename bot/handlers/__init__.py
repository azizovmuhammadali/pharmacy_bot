from .admin.orders import router as admin_orders_router
from .admin.products import router as admin_products_router
from .user.cart import router as cart_router
from .user.catalog import router as catalog_router
from .user.checkout import router as checkout_router
from .user.location import router as location_router
from .user.product import router as product_router
from .user.search import router as search_router
from .user.start import router as start_router

routers = [
    start_router,
    catalog_router,
    search_router,
    product_router,
    cart_router,
    checkout_router,
    location_router,
    admin_products_router,
    admin_orders_router,
]
