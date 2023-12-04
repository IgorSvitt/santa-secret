from aiogram.fsm.state import State, StatesGroup


class MessageState(StatesGroup):
    text = State()
    answer = State()
