from aiogram.fsm.state import State, StatesGroup


class UserSetting(StatesGroup):
    name = State()
    room = State()
    link_to_vk = State()
    info = State()