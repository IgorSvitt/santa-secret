from aiogram.fsm.state import State, StatesGroup


class User(StatesGroup):
    name = State()
    link_to_vk = State()
    room = State()
