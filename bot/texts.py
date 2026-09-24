# ============ REPLY KEYBOARD BUTTONS ============
BTN_CATALOG = "🗂 Katalog"
BTN_SEARCH = "🔎 Qidiruv"
BTN_CART = "🛒 Savat"
BTN_NEAREST_BRANCH = "📍 Eng yaqin filial"
BTN_SEND_CONTACT = "📱 Telefon raqamni yuborish"

# ============ INLINE BUTTONS ============
BTN_BACK_CATEGORIES = "⬅️ Kategoriyalarga qaytish"
BTN_ADD_TO_CART = "🛒 Savatga qo'shish"
BTN_BACK_CATALOG = "⬅️ Katalogga qaytish"
BTN_CHECKOUT = "✅ Buyurtma berish"
BTN_CONTINUE_SHOPPING = "⬅️ Xaridni davom ettirish"
BTN_DEACTIVATE = "🗑 O'chirish"
BTN_BACK_PRODUCTS = "⬅️ Mahsulotlarga qaytish"
BTN_BACK_ADMIN = "⬅️ Admin menyu"
BTN_BACK_ORDERS = "⬅️ Buyurtmalarga qaytish"

# ============ USER MESSAGES ============
WELCOME = (
    "Dorixona botiga xush kelibsiz!\n\n"
    "Bu yerda siz:\n"
    "- Katalog bo'ylab ko'rib chiqishingiz\n"
    "- Dori qidirishingiz\n"
    "- Mahsulotlarni savatga qo'shishingiz\n"
    "- Buyurtma berishingiz\n"
    "- Eng yaqin filialni topishingiz mumkin"
)

CHOOSE_CATEGORY = "Kategoriyani tanlang:"
NO_CATEGORIES = "Kategoriyalar topilmadi."
AVAILABLE_PRODUCTS = "Mavjud mahsulotlar:"
NO_PRODUCTS_IN_CATEGORY = "Bu kategoriyada mahsulotlar yo'q."
NO_PRODUCTS_FOUND = "Hech qanday mahsulot topilmadi."
SEND_MEDICINE_NAME = "Qidirish uchun dori nomini yuboring."
SEARCH_RESULTS = "Qidiruv natijalari:"

PRODUCT_PRICE = "Narxi"
PRODUCT_STOCK = "Omborda"
PRODUCT_DESCRIPTION = "Tavsif"
PRODUCT_COMPOSITION = "Tarkibi"
PRODUCT_USAGE = "Qo'llash bo'yicha ko'rsatma"

CART_EMPTY = "Savatingiz bo'sh."
CART_TITLE = "🛒 Savatingiz:"
CART_TOTAL = "Jami"
CART_ADDED = "Savatga qo'shildi."
CART_OUT_OF_STOCK = "Mahsulot omborda yo'q."

SEND_PHONE = "Iltimos, telefon raqamingizni yuboring."
INVALID_PHONE = "Iltimos, to'g'ri telefon raqamini yuboring."
CHOOSE_DELIVERY = "Yetkazib berish usulini tanlang:"
ENTER_ADDRESS = "Yetkazib berish manzilini kiriting."
CHOOSE_BRANCH = "Olib ketish filialini tanlang:"
NO_BRANCHES_USE_ADDRESS = "Filiallar topilmadi. Iltimos, yetkazib berish manzilini kiriting."
CHECKOUT_ERROR = "Buyurtma xatosi. Qayta urinib ko'ring."
CART_EMPTY_ALERT = "Savatingiz bo'sh."

ORDER_SUCCESS = (
    "✅ Buyurtma muvaffaqiyatli qabul qilindi.\n\n"
    "Buyurtma raqami: #{order_id}\n"
    "Holat: {status}\n\n"
    "Tez orada farmatsevtimiz siz bilan bog'lanadi."
)
ORDER_ERROR = "❌ {error}"

NEAREST_BRANCH_TITLE = "📍 Eng yaqin filial:"
BRANCH_ADDRESS = "Manzil"
BRANCH_PHONE = "Telefon"
BRANCH_DISTANCE = "Masofa"

# ============ ADMIN MESSAGES ============
ADMIN_PANEL = "Admin panel"
ADMIN_ADD_PRODUCT = "➕ Mahsulot qo'shish"
ADMIN_PRODUCTS = "📦 Mahsulotlar"
ADMIN_ORDERS = "🧾 Buyurtmalar"

SEND_PRODUCT_NAME = "Mahsulot nomini yuboring."
SEND_PRICE = "Narxni yuboring. Masalan: 15.50"
INVALID_PRICE = "Noto'g'ri narx. Masalan: 15.50"
PRICE_MUST_BE_POSITIVE = "Narx noldan katta bo'lishi kerak."
SEND_STOCK = "Ombordagi miqdorni yuboring."
INVALID_STOCK = "Noto'g'ri miqdor."
STOCK_NEGATIVE = "Miqdor manfiy bo'la olmaydi."
SEND_DESCRIPTION = "Tavsifni yuboring yoki o'tkazib yuborish uchun '-' yozing."
SEND_COMPOSITION = "Tarkibni yuboring yoki o'tkazib yuborish uchun '-' yozing."
SEND_USAGE = "Qo'llash ko'rsatmasini yuboring yoki o'tkazib yuborish uchun '-' yozing."
PRODUCT_CREATED = "✅ Mahsulot qo'shildi.\nID: {product_id}"
PRODUCTS_LIST = "Mahsulotlar:"
PRODUCT_NOT_FOUND = "Mahsulot topilmadi."
SEND_NEW_VALUE = "{label} uchun yangi qiymatni yuboring:"
INVALID_VALUE = "Noto'g'ri qiymat."
PRODUCT_UPDATED = "✅ Mahsulot yangilandi."
PRODUCT_DEACTIVATED = "Mahsulot o'chirildi."
EDIT_ERROR = "Tahrirlash xatosi."

ORDERS_LIST = "Buyurtmalar:"
ORDER_NOT_FOUND = "Buyurtma topilmadi."
STATUS_UPDATED = "Holat yangilandi."
ORDER_STATUS_UPDATED = "Buyurtma #{order_id} holati yangilandi: {status}"
INVALID_STATUS = "Noto'g'ri holat."

# ============ LABELS ============
FIELD_LABELS = {
    "price": "💵 Narx",
    "stock": "📦 Ombor",
    "name": "📝 Nom",
    "description": "📄 Tavsif",
    "composition": "🧪 Tarkib",
    "usage_instructions": "ℹ️ Qo'llash",
}

STATUS_LABELS = {
    "Pending": "⏳ Kutilmoqda",
    "Accepted": "✅ Qabul qilindi",
    "Shipped": "🚚 Yuborildi",
    "Completed": "🏁 Bajarildi",
    "Cancelled": "❌ Bekor qilindi",
}

DELIVERY_LABELS = {
    "delivery": "🚚 Yetkazib berish",
    "pickup": "🏪 Olib ketish",
}
