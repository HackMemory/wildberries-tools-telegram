from typing import List, Tuple

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from aiogram import executor
from loguru import logger
import logging

from utils.db.db_api import Users

from data import config
from utils.db.db_api.payments import Payments


# noinspection PyUnusedLocal
async def on_startup(dp: Dispatcher):
    import filters
    import handlers
    filters.setup(dp)
    handlers.errors.setup(dp)
    handlers.user.setup(dp)

    await Users.create_table_users()
    await Payments.create_table_payments()


async def on_shutdown(dp: Dispatcher):
    pass


if __name__ == '__main__':
    #logging.basicConfig(level=logging.DEBUG)

    bot = Bot(config.BOT_TOKEN, parse_mode=ParseMode.HTML)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    executor.start_polling(dp, on_startup=on_startup)
