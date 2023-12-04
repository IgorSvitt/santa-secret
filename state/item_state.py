from aiogram.fsm.state import State, StatesGroup


class Item(StatesGroup):
    name = State()


class ItemChange(StatesGroup):
    id = State()
    new_name = State()


class ItemDelete(StatesGroup):
    id = State()