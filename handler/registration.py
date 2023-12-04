from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from state.registration_state import User
from keyboard import for_main
from data import user_db
router = Router()
users = user_db.UserDB()


@router.callback_query(F.data == "participate")
async def participate_handler(callback_query: CallbackQuery, state: FSMContext) -> None:
    await callback_query.message.edit_reply_markup()
    await callback_query.message.answer(
        "Для начала, давай познакомимся. Как тебя зовут (Имя и Фамилия)? 🎅"
    )
    await state.set_state(User.name)


@router.message(User.name)
async def name_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await message.answer(
        "Отлично, теперь введи свой номер комнаты 🏠"
    )
    await state.set_state(User.room)


@router.message(User.room)
async def room_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(room=message.text)
    await message.answer(
        "Отлично, теперь введи ссылку на свой профиль в ВК 📱"
    )
    await state.set_state(User.link_to_vk)


@router.message(User.link_to_vk)
async def link_to_vk_handler(message: Message, state: FSMContext) -> None:
    await state.update_data(link_to_vk=message.text)
    await message.answer(
        "Отлично, теперь ты зарегистрирован в нашей системе.\n"
        "Скоро мы начнем рассылку новостей и важных событий.\n",
        reply_markup=for_main.main_buttons()
    )
    data = await state.get_data()
    await users.add_user(
        userid=message.from_user.id,
        name=data.get("name"),
        room=data.get("room"),
        link_to_vk=data.get("link_to_vk"),
        count_messages=0,
        username=message.from_user.username
    )
    await state.clear()



