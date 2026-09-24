from aiogram.fsm.state import State, StatesGroup


class SearchStates(StatesGroup):
    waiting_query = State()


class CheckoutStates(StatesGroup):
    phone = State()
    delivery = State()
    address = State()
    branch = State()


class AddProductStates(StatesGroup):
    name = State()
    category = State()
    price = State()
    stock = State()
    description = State()
    composition = State()
    usage = State()


class EditProductStates(StatesGroup):
    value = State()
