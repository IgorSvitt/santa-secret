from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram import Router, F, Bot
from keyboard import for_admin
from data import user_db
import random
from config import ADMIN_USERNAME

router = Router()
users = user_db.UserDB()


@router.message(Command("play"))
async def play_handler(message: Message, state: FSMContext, bot: Bot) -> None:
    if message.from_user.username == ADMIN_USERNAME:
        all_users = await users.get_users()
        user_list = [x[0] for x in all_users]
        result = secret_santa_partners(user_list)
        for userid in user_list:
            try:
                await bot.send_message(
                    chat_id=userid,
                    text="Тайный Санта начался! 🎅\n"
                         "Ты можешь узнать, кому ты даришь подарок, нажав на кнопку\n\n🎅 Кому я дарю подарок?"
                )
            except Exception as e:
                print(e)
                continue
        for giver, receiver in result:
            await users.change_santa(giver, receiver)
            print(f"{giver} дарит подарок {receiver}")
    else:
        await message.answer(
            "Не балуйся, а то получишь по попе 😡",
        )


@router.message(Command("getusers"))
async def get_users(message: Message, state: FSMContext, bot: Bot) -> None:
    if message.from_user.username == ADMIN_USERNAME:
        all_users = await users.get_users()
        for user in all_users:
            await message.answer(f"{user[0]} - {user[1]}")
    else:
        await message.answer(
            "Не балуйся, а то получишь по попе 😡",
        )


def secret_santa_partners(participants):
    shuffled_list = participants.copy()
    random.shuffle(shuffled_list)

    pairs = []
    for i in range(len(participants)):
        giver = participants[i]
        receiver = shuffled_list[i]

        # Ensure a person doesn't buy a gift for themselves
        if giver == receiver:
            return secret_santa_partners(participants)

        pairs.append((giver, receiver))

    return pairs
