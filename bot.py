from typing import List, Tuple

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode
from aiogram import executor
from loguru import logger

from data import config


# noinspection PyUnusedLocal
async def on_startup(dp: Dispatcher):
    import filters
    import handlers
    filters.setup(dp)
    handlers.errors.setup(dp)
    handlers.user.setup(dp)


async def on_shutdown(dp: Dispatcher):
    pass


if __name__ == '__main__':
    bot = Bot(config.BOT_TOKEN, parse_mode=ParseMode.HTML, validate_token=True)
    storage = MemoryStorage()
    dp = Dispatcher(bot, storage=storage)

    executor.start_polling(dp, on_startup=on_startup)
