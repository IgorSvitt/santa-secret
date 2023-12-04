from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F
from state.user_state import MessageState
from keyboard import for_main
from data import user_db, item_db

router = Router()
users = user_db.UserDB()
items = item_db.ItemDB()


@router.message(F.text == "🎅 Кому я дарю подарок?")
async def my_santa_handler(message: Message, state: FSMContext) -> None:
    try:
        me = await users.get_user(message.from_user.id)
        my_santa_id = me[7]
        santa = await users.get_santa(my_santa_id)
        if santa:
            user_items = await items.get_items(santa[0])
            text = ""
            for i in range(len(user_items)):
                text += f"{i + 1}) <b>{user_items[i][0]}</b>\n\n"

            if text == "":
                text = "У него нет желаний 😔"

            await message.answer(
                f"Ты даришь подарок <b>{santa[1]}</b>🎅 \n\n"
                f"Его username: @{santa[2]}\n"
                f"Информация о нем: {santa[3]}\n"
                f"Его комната: {santa[4]}\n"
                f"Его ВК: {santa[5]}\n\n"
                f"Его желания:\n{text}",
                reply_markup=for_main.main_buttons()
            )
        else:
            await message.answer(
                "Тайный Санта еще не стартовал\n",
                reply_markup=for_main.main_buttons()
            )
    except Exception as e:
        print(e)
        await message.answer(
            "Ой, что-то пошло не так 😔\n",
            reply_markup=for_main.main_buttons()
        )


@router.message(F.text == "🎄 Написать сообщение")
async def write_message_handler(message: Message, state: FSMContext) -> None:
    # await message.answer(
    #     "Напиши сообщение, которое хочешь отправить челику 🎅",
    #     reply_markup=for_main.cancel_keyboard()
    # )
    # await state.set_state(MessageState.text)
    await message.answer("В разработке 🚧")


@router.message(MessageState.text)
async def write_message_handler(message: Message, state: FSMContext) -> None:
    try:
        me = await users.get_user(message.from_user.id)
        my_santa_id = me[7]
        santa = await users.get_santa(my_santa_id)
        if santa:
            await message.bot.send_message(
                chat_id=santa[0],
                text=f"Тебе пришло сообщение от твоего Санты 🎅\n\n"
                     f"{message.text}",
                reply_markup=for_main.main_buttons()
            )
        else:
            await message.answer(
                "Тайный Санта еще не стартовал\n",
                reply_markup=for_main.main_buttons()
            )
    except Exception as e:
        print(e)
        await message.answer(
            "Ой, что-то пошло не так 😔\n",
            reply_markup=for_main.main_buttons()
        )
    await state.clear()


@router.callback_query(F.data == "send_answer")
async def send_answer_handler(call: CallbackQuery, state: FSMContext) -> None:
    await call.message.edit_reply_markup()
    await call.message.answer(
        "Напиши сообщение, которое хочешь отправить Санте 🎅",
        reply_markup=for_main.cancel_keyboard()
    )
    await state.set_state(MessageState.answer)


@router.message(MessageState.answer)
async def send_answer_handler(message: Message, state: FSMContext) -> None:
    try:
        me = await users.get_user(message.from_user.id)
        my_santa_id = me[6]
        santa = await users.get_santa(my_santa_id)
        if santa:
            await message.bot.send_message(
                chat_id=santa[0],
                text=f"Тебе пришло сообщение от твоего Санты 🎅\n\n"
                     f"{message.text}",
                reply_markup=for_main.main_buttons()
            )
        else:
            await message.answer(
                "Тайный Санта еще не стартовал\n",
                reply_markup=for_main.main_buttons()
            )
    except Exception as e:
        print(e)
        await message.answer(
            "Ой, что-то пошло не так 😔\n",
            reply_markup=for_main.main_buttons()
        )
    await state.clear()
