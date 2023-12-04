from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from keyboard import for_settings
from data import user_db
from state import settings_state

router = Router()
user = user_db.UserDB()


@router.message(F.text == "Мои данные 📝")
@router.message(F.text == "⚙ Изменить информацию о себе")
async def my_data(message: Message, state: FSMContext) -> None:
    info = await user.get_user(message.from_user.id)
    name = info[1]
    room = info[4]
    link_to_vk = info[5]
    about = info[3]

    await message.answer(
        text="Мои данные 📝:\n"
             f"Имя: <code>{name}</code>\n"
             f"Комната: <code>{room}</code>\n"
             f"Информация о себе: <code>{about}</code>\n"
             f"Ссылка на ВК: <code>{link_to_vk}</code>\n\n",
        reply_markup=for_settings.setting_keyboards()
    )


@router.message(F.text == "Изменить имя ✏")
async def change_name(message: Message, state: FSMContext) -> None:
    await message.answer(
        text="Введите новое имя",
        reply_markup=for_settings.cancel_keyboard()
    )
    await state.set_state(settings_state.UserSetting.name)


@router.message(settings_state.UserSetting.name)
async def change_name(message: Message, state: FSMContext) -> None:
    try:
        await user.change_name(message.from_user.id, message.text)
        await message.answer(
            text="Имя успешно изменено ✅",
            reply_markup=for_settings.setting_keyboards()
        )
    except Exception as e:
        print(e)
        await message.answer(
            text="Ой, что-то пошло не так 😔\n",
            reply_markup=for_settings.setting_keyboards()
        )

    await state.clear()


@router.message(F.text == "Изменить номер комнаты ✏")
async def change_room(message: Message, state: FSMContext) -> None:
    await message.answer(
        text="Введите новую комнату",
        reply_markup=for_settings.cancel_keyboard()
    )
    await state.set_state(settings_state.UserSetting.room)


@router.message(settings_state.UserSetting.room)
async def change_room(message: Message, state: FSMContext) -> None:
    try:
        await user.change_room(message.from_user.id, message.text)
        await message.answer(
            text="Комната успешно изменена ✅",
            reply_markup=for_settings.setting_keyboards()
        )
    except Exception as e:
        print(e)
        await message.answer(
            text="Ой, что-то пошло не так 😔\n",
            reply_markup=for_settings.setting_keyboards()
        )

    await state.clear()


@router.message(F.text == "Изменить ссылку на ВК ✏")
async def change_link_to_vk(message: Message, state: FSMContext) -> None:
    await message.answer(
        text="Введите новую ссылку на ВК",
        reply_markup=for_settings.cancel_keyboard()
    )
    await state.set_state(settings_state.UserSetting.link_to_vk)


@router.message(settings_state.UserSetting.link_to_vk)
async def change_link_to_vk(message: Message, state: FSMContext) -> None:
    try:
        await user.change_link_to_vk(message.from_user.id, message.text)
        await message.answer(
            text="Ссылка на ВК успешно изменена ✅",
            reply_markup=for_settings.setting_keyboards()
        )
    except Exception as e:
        print(e)
        await message.answer(
            text="Ой, что-то пошло не так 😔\n",
            reply_markup=for_settings.setting_keyboards()
        )

    await state.clear()


@router.message(F.text == "Изменить информацию о себе ✏")
async def change_info(message: Message, state: FSMContext) -> None:
    await message.answer(
        text="Введите информацию о себе",
        reply_markup=for_settings.cancel_keyboard()
    )
    await state.set_state(settings_state.UserSetting.info)


@router.message(settings_state.UserSetting.info)
async def change_info(message: Message, state: FSMContext) -> None:
    try:
        await user.change_about(message.from_user.id, message.text)
        await message.answer(
            text="Информация о себе успешно изменена ✅",
            reply_markup=for_settings.setting_keyboards()
        )
    except Exception as e:
        print(e)
        await message.answer(
            text="Ой, что-то пошло не так 😔\n",
            reply_markup=for_settings.setting_keyboards()
        )

    await state.clear()


@router.callback_query(F.data == "cancel_setting")
async def cancel_setting(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.edit_reply_markup()
    await call.message.delete()
    await call.message.answer(
        text="Действие отменено ❌",
        reply_markup=for_settings.setting_keyboards()
    )
    await state.clear()
