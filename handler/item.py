from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from keyboard import for_item
from data import item_db
from state.item_state import Item, ItemChange, ItemDelete

router = Router()
item = item_db.ItemDB()


@router.message(F.text == "🎁 Мой список желаний")
async def my_item_handler(message: Message, state: FSMContext) -> None:
    items = await item.get_items(message.from_user.id)
    if not items:
        await message.answer(
            "Твой список желаний пуст 😔\n\n",
            reply_markup=for_item.item_keyboards()
        )
    else:
        text = ""
        for i in range(len(items)):
            text += f"{i + 1}) <b>{items[i][0]}</b>\n"
        await message.answer(
            "Вот твой список желаний:\n"
            f"{text}",
            reply_markup=for_item.item_keyboards()
        )


@router.message(F.text == "Добавить новое желание 🎁")
async def add_item_handler(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Напиши, что ты хочешь получить в подарок 🎁",
        reply_markup=for_item.cancel_keyboard()
    )
    await state.set_state(Item.name)


@router.message(Item.name)
async def add_item_handler(message: Message, state: FSMContext) -> None:
    try:
        await item.add_item(message.from_user.id, message.text)
        await message.answer(
            "Твое желание добавлено в список 🎁",
            reply_markup=for_item.item_keyboards()
        )
        items = await item.get_items(message.from_user.id)
        text = ""
        for i in range(len(items)):
            text += f"{i + 1}) <b>{items[i][0]}</b>\n"
        await message.answer(
            "Вот твой список желаний:\n"
            f"{text}",
            reply_markup=for_item.item_keyboards()
        )
    except Exception as e:
        print(e)
        await message.answer(
            "Ой, что-то пошло не так 😔\n",
            reply_markup=for_item.item_keyboards()
        )
    await state.clear()


@router.message(F.text == "Изменить желание ✏")
async def change_item_handler(message: Message, state: FSMContext) -> None:
    items = await item.get_items(message.from_user.id)
    if items == "":
        await message.answer(
            "Твой список желаний пуст 😔\n\n",
            reply_markup=for_item.item_keyboards()
        )
    else:
        names = []
        ids = []
        for i in range(len(items)):
            names.append(items[i][0])
            ids.append(items[i][1])
        await message.answer(
            "Выбери желания, которое ты хочешь удалить ❌",
            reply_markup=for_item.update_item_keyboard(names, ids)
        )


@router.callback_query(F.data.startswith("update_item_"))
async def update_item_handler(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.edit_reply_markup()
    await callback.message.answer(
        "Напиши новое желание ✏",
        reply_markup=for_item.cancel_keyboard()
    )
    await state.update_data(id=int(callback.data.split("_")[2]))
    await state.set_state(ItemChange.new_name)


@router.message(ItemChange.new_name)
async def update_item_handler(message: Message, state: FSMContext) -> None:
    data = await state.get_data()
    await item.change_item(itemid=data['id'], new_name=message.text)
    await message.answer(
        "Твое желание изменено ✏",
        reply_markup=for_item.item_keyboards()
    )
    await state.clear()


@router.message(F.text == "Удалить желание ❌")
async def delete_item_handler(message: Message, state: FSMContext) -> None:
    items = await item.get_items(message.from_user.id)
    if items == "":
        await message.answer(
            "Твой список желаний пуст 😔\n\n",
            reply_markup=for_item.item_keyboards()
        )
    else:
        names = []
        ids = []
        for i in range(len(items)):
            names.append(items[i][0])
            ids.append(items[i][1])
        await message.answer(
            "Выбери желания, которое ты хочешь удалить ❌",
            reply_markup=for_item.delete_item_keyboard(names, ids)
        )


@router.callback_query(F.data.startswith("delete_item_"))
async def delete_item_handler(callback: CallbackQuery, state: FSMContext) -> None:
    try:
        await callback.message.edit_reply_markup()
        delete_item_id = callback.data.split("_")[2]
        await item.delete_item(int(delete_item_id))
        await callback.message.answer(
            "Твое желание удалено ✅",
            reply_markup=for_item.item_keyboards()
        )
    except Exception as e:
        print(e)
        await callback.message.answer(
            "Такого желания нет ❌",
            reply_markup=for_item.item_keyboards()
        )

    await state.clear()


@router.callback_query(F.data == "cancel_item")
async def cancel_handler(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.edit_reply_markup()
    await call.message.delete()
    await state.clear()
    await call.message.answer(
        text="Действие отменено ❌",
        reply_markup=for_item.item_keyboards()
    )
    await state.clear()
