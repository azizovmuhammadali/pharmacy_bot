from bot.handlers.admin import start as admin_start
from bot.handlers.user import start, catalog, product, cart, checkout, search, location

routers = [
    start.router,
    catalog.router,
    product.router,
    cart.router,
    checkout.router,
    search.router,
    location.router,
    admin_start.router,  # Admin router qo'shildi
]
