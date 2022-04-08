from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart, CommandHelp
import states.user
from keyboards.inline.callbacks import *
from states.user import user

from .help import bot_help
from .start import *
from .my_items import *


def setup(dp: Dispatcher):
    dp.register_message_handler(bot_start, CommandStart())

    dp.register_callback_query_handler(main_menu, menu_cd.filter(action="main-menu-back"))
    dp.register_callback_query_handler(main_menu, menu_cd.filter(action="main-menu-open"))

    dp.register_callback_query_handler(choose_my_items, menu_cd.filter(action="main-menu-items"))
    dp.register_callback_query_handler(profile, menu_cd.filter(action="main-menu-profile"))

    dp.register_callback_query_handler(my_items, menu_cd.filter(action="menu-items-choose"))
    dp.register_callback_query_handler(custom_item_id, menu_cd.filter(action="menu-item-custom"))
    dp.register_message_handler(process_custom_item_id, state=user.FindItem.item_id)

    dp.register_callback_query_handler(remove_token_confirm, menu_cd.filter(action="token-yes"))
    dp.register_callback_query_handler(remove_token, menu_cd.filter(action="main-menu-remove-token"))
    dp.register_callback_query_handler(add_token, menu_cd.filter(action="main-menu-add-token"))
    dp.register_message_handler(process_token, state=user.Token.token)

    dp.register_callback_query_handler(my_items, menu_cd.filter(action="page"))
    dp.register_callback_query_handler(select_item, item_cd.filter(action="select-item"))
    #dp.register_message_handler(bot_help, CommandHelp())
