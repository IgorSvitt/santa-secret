from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def main_buttons() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="🎁 Мой список желаний"))
    builder.row(types.KeyboardButton(text="🎄 Написать сообщение"))
    builder.row(types.KeyboardButton(text="🎅 Кому я дарю подарок?"))
    builder.row(types.KeyboardButton(text="⚙ Изменить информацию о себе"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def cancel_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Отмена", callback_data="cancel_setting"))
    return builder.as_markup()


def send_answer() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Ответить", callback_data="send_answer"))
    return builder.as_markup()
