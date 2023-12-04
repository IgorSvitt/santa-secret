from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from aiogram import Router, F, Bot
from aiogram.filters import Command
from config import ADMIN_USERNAME

from keyboard import for_start, for_main

from data import user_db

router = Router()


@router.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    users = user_db.UserDB()
    if await users.get_user(message.from_user.id) is None and message.from_user.username != ADMIN_USERNAME:
        await message.answer(
            "Хоу-хоу-хоу 🎅\n\n"
            "Вот и начинается по чуть-чуть сезон игры в Тайного Санту\n\n"
            "Здесь ты сможешь подарить и получить праздничные сюрпризы от своего тайного Санты.🎁\n\n"
            "Чтобы начать, нажми кнопку <b>участвовать</b> и следуй инструкциям. После завершения регистрации ты "
            "узнаешь, "
            "кому будешь дарить подарок!\n\n "
            "Удачи и пусть праздник начнется! 🌟",
            reply_markup=for_start.participate_key()
        )
    else:
        await message.answer(
            f"Добро пожаловать обратно, {message.from_user.full_name}! 🎉\n\n"
            "Рад видеть тебя вновь в игре в Тайного Санту. Ты уже зарегистрирован, и теперь можешь следить за своими "
            "подарками и готовиться к тому моменту, когда сможешь порадовать своего Тайного Санту своим подарком. "
            "🎁\n\n "
            "Если у тебя есть какие-либо вопросы или нужна помощь, не стесняйся спросить. Удачи в игре и пусть "
            "праздник продлится весело! 🌟",
            reply_markup=for_main.main_buttons()
        )


@router.message(F.text == "Вернуться в главное меню 🏠")
async def return_to_main_menu(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        text="Выбери действие",
        reply_markup=for_main.main_buttons()
    )


