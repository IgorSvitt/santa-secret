from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def item_keyboards() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(types.KeyboardButton(text="Добавить новое желание 🎁"),
                types.KeyboardButton(text="Удалить желание ❌"))
    builder.row(types.KeyboardButton(text="🎁 Мой список желаний"))
    builder.row(types.KeyboardButton(text="Изменить желание ✏"),
                types.KeyboardButton(text="Вернуться в главное меню 🏠"))
    return builder.as_markup(resize_keyboard=True)


def cancel_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(types.InlineKeyboardButton(text="Отмена", callback_data="cancel_item"))
    return builder.as_markup()


def delete_item_keyboard(item_names, item_ids) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for i in range(len(item_names)):
        builder.row(types.InlineKeyboardButton(text=f"{item_names[i]}", callback_data=f"delete_item_{item_ids[i]}"))
    builder.row(types.InlineKeyboardButton(text="Отмена", callback_data="cancel_item"))
    return builder.as_markup()


def update_item_keyboard(item_names, item_ids) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for i in range(len(item_names)):
        builder.row(types.InlineKeyboardButton(text=f"{item_names[i]}", callback_data=f"update_item_{item_ids[i]}"))
    builder.row(types.InlineKeyboardButton(text="Отмена", callback_data="cancel_item"))
    return builder.as_markup()
