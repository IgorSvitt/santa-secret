from aiogram import types
from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def participate_key() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Участвовать", callback_data="participate"))
    return builder.as_markup()
