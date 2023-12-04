from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def setting_keyboards() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="Изменить имя ✏"),
                types.KeyboardButton(text="Изменить номер комнаты ✏"))
    builder.row(types.KeyboardButton(text="Мои данные 📝"))
    builder.row(types.KeyboardButton(text="Изменить ссылку на ВК ✏"),
                types.KeyboardButton(text="Изменить информацию о себе ✏"),
                types.KeyboardButton(text="Вернуться в главное меню 🏠"))
    return builder.as_markup(resize_keyboard=True)


def cancel_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Отмена", callback_data="cancel_setting"))
    return builder.as_markup()
