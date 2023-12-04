from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from config import BOT_TOKEN
from data import user_db, item_db, message_db
from handler import registration, start_bot, item, settings, admin_command, user_command

import logging


async def start():
    logging.basicConfig(level=logging.INFO)
    await user_db.UserDB().create_table()
    await item_db.ItemDB().create_table()
    await message_db.MessageDB().create_table()
    bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(admin_command.router)
    dp.include_router(start_bot.router)
    dp.include_router(registration.router)
    dp.include_router(item.router)
    dp.include_router(user_command.router)
    dp.include_router(settings.router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

