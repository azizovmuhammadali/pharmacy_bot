from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from bot.db.base import async_session_factory
from bot.db.models import User as UserModel
from bot.services import branch as branch_service
from bot.services import cart as cart_service
from bot.services import order as order_service
from bot.services import product as product_service
from web.auth import current_user

router = APIRouter(prefix="/api", tags=["api"])


async def get_session():
    async with async_session_factory() as session:
        yield session


async def ensure_user(session: AsyncSession, user: dict) -> int:
    uid = int(user["id"])
    row = await session.get(UserModel, uid)
    if not row:
        full = f"{user.get('first_name') or ''} {user.get('last_name') or ''}".strip()
        row = UserModel(id=uid, full_name=full or "Unknown", username=user.get("username"))
        session.add(row)
        await session.commit()
    return uid


def _brief(p) -> dict:
    return {
        "id": p.id,
        "name": p.name,
        "price": float(p.price),
        "stock": p.stock,
        "category_id": p.category_id,
    }


@router.get("/me")
async def me(user: dict = Depends(current_user), session: AsyncSession = Depends(get_session)):
    uid = await ensure_user(session, user)
    return {"id": uid, "name": user.get("first_name")}


@router.get("/categories")
async def categories(session: AsyncSession = Depends(get_session)):
    cats = await product_service.get_categories(session)
    return [{"id": c.id, "name": c.name} for c in cats]


@router.get("/products")
async def products(
    category_id: int | None = None,
    q: str | None = None,
    session: AsyncSession = Depends(get_session),
):
    if q:
        items = await product_service.search_products(session, q)
    elif category_id:
        items = await product_service.get_products_by_category(session, category_id)
    else:
        items = await product_service.get_products(session)
    return [_brief(p) for p in items]


@router.get("/products/{product_id}")
async def product_detail(product_id: int, session: AsyncSession = Depends(get_session)):
    p = await product_service.get_product(session, product_id)
    if not p or not p.is_active:
        raise HTTPException(status_code=404, detail="Mahsulot topilmadi")
    return {
        **_brief(p),
        "description": p.description,
        "composition": p.composition,
        "usage_instructions": p.usage_instructions,
    }


@router.get("/cart")
async def cart(user: dict = Depends(current_user), session: AsyncSession = Depends(get_session)):
    uid = await ensure_user(session, user)
    items = await cart_service.get_cart_items(session, uid)
    out = []
    total = 0.0
    for it in items:
        line = float(it.product.price) * it.quantity
        total += line
        out.append({
            "item_id": it.id,
            "product_id": it.product_id,
            "name": it.product.name,
            "price": float(it.product.price),
            "quantity": it.quantity,
            "line_total": round(line, 2),
        })
    return {"items": out, "total": round(total, 2)}


class AddBody(BaseModel):
    product_id: int
    quantity: int = 1


@router.post("/cart/add")
async def cart_add(body: AddBody, user: dict = Depends(current_user), session: AsyncSession = Depends(get_session)):
    uid = await ensure_user(session, user)
    ok = await cart_service.add_to_cart(session, uid, body.product_id, body.quantity)
    if not ok:
        raise HTTPException(status_code=400, detail="Mahsulot omborda yo'q")
    return {"ok": True}


class UpdBody(BaseModel):
    item_id: int
    delta: int


@router.post("/cart/update")
async def cart_update(body: UpdBody, user: dict = Depends(current_user), session: AsyncSession = Depends(get_session)):
    uid = await ensure_user(session, user)
    await cart_service.change_quantity(session, body.item_id, uid, body.delta)
    return {"ok": True}


@router.delete("/cart/{item_id}")
async def cart_remove(item_id: int, user: dict = Depends(current_user), session: AsyncSession = Depends(get_session)):
    uid = await ensure_user(session, user)
    await cart_service.remove_item(session, item_id, uid)
    return {"ok": True}


class CheckoutBody(BaseModel):
    phone: str
    delivery_method: str
    address: str | None = None
    branch_id: int | None = None


@router.post("/checkout")
async def checkout(body: CheckoutBody, user: dict = Depends(current_user), session: AsyncSession = Depends(get_session)):
    uid = await ensure_user(session, user)
    full = f"{user.get('first_name') or ''} {user.get('last_name') or ''}".strip() or "Unknown"
    try:
        order = await order_service.create_order(
            session, uid, full, body.phone, body.delivery_method, body.address, body.branch_id
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    return {"order_id": order.id, "status": order.status}


@router.get("/branches")
async def branches(session: AsyncSession = Depends(get_session)):
    bs = await branch_service.get_branches(session)
    return [{"id": b.id, "name": b.name, "address": b.address, "phone": b.phone} for b in bs]

# --- ADMIN ENDPOINTS ---

@router.get("/admin/stats")
async def admin_stats(user: dict = Depends(current_user), session: AsyncSession = Depends(get_session)):
    if int(user["id"]) not in config.admin_ids:
        raise HTTPException(status_code=403, detail="Admin huquqi yo'q")
    
    # Oddi statistika (keyinroq murakkablashtiramiz)
    from bot.db.models import Product, Order
    from sqlalchemy import func
    
    product_count = await session.execute(func.count(Product.id))
    order_count = await session.execute(func.count(Order.id))
    
    return {
        "total_products": product_count.scalar(),
        "total_orders": order_count.scalar(),
        "admin_name": user.get("first_name")
    }

@router.get("/admin/orders")
async def admin_orders(user: dict = Depends(current_user), session: AsyncSession = Depends(get_session)):
    if int(user["id"]) not in config.admin_ids:
        raise HTTPException(status_code=403, detail="Admin huquqi yo'q")
    
    from bot.db.models import Order
    # So'nggi 50 ta buyurtma
    result = await session.execute(
        select(Order).order_by(Order.created_at.desc()).limit(50)
    )
    orders = result.scalars().all()
    
    return [{
        "id": o.id,
        "user_id": o.user_id,
        "total": float(o.total),
        "status": o.status,
        "created_at": o.created_at.isoformat() if o.created_at else None
    } for o in orders]
