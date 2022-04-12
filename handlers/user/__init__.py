from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart, CommandHelp
import states.user
from aiogram.dispatcher.filters import Text
from aiogram.types.message import ContentTypes
from keyboards.inline.callbacks import *
from states.user import user

from .help import bot_help
from .start import *
from .payment import *
from .my_items import *


def setup(dp: Dispatcher):
    dp.register_message_handler(bot_start, CommandStart())

    dp.register_message_handler(cancel_handler, state='*', commands='cancel')
    dp.register_message_handler(cancel_handler, Text(equals='cancel', ignore_case=True), state='*')

    dp.register_callback_query_handler(main_menu, menu_cd.filter(action="main-menu-back"))
    dp.register_callback_query_handler(main_menu, menu_cd.filter(action="main-menu-open"))

    dp.register_callback_query_handler(choose_my_items, menu_cd.filter(action="main-menu-items"))
    dp.register_callback_query_handler(profile, menu_cd.filter(action="main-menu-profile"))

    dp.register_callback_query_handler(my_items, menu_cd.filter(action="menu-items-choose"))
    dp.register_callback_query_handler(custom_item_id, menu_cd.filter(action="menu-item-custom"))
    dp.register_message_handler(process_custom_item_id, state=user.FindItem.item_id)

    dp.register_callback_query_handler(change_name, changename_cd.filter(a="icn"))
    dp.register_message_handler(process_change_name, state=user.ChangeItem.item_name)

    dp.register_callback_query_handler(remove_token_confirm, menu_cd.filter(action="token-yes"))
    dp.register_callback_query_handler(remove_token, menu_cd.filter(action="main-menu-remove-token"))
    dp.register_callback_query_handler(add_token, menu_cd.filter(action="main-menu-add-token"))
    dp.register_message_handler(process_token, state=user.Token.token)

    dp.register_callback_query_handler(my_items, menu_cd.filter(action="page"))
    dp.register_callback_query_handler(select_item, item_cd.filter(action="select-item"))

    dp.register_callback_query_handler(select_country_char, menu_cd.filter(action="country-list"))
    dp.register_callback_query_handler(select_country_list, changename_cd.filter(a="scc"))
    dp.register_callback_query_handler(change_name, changename_cd.filter(a="sc"))

    dp.register_callback_query_handler(select_payment, menu_cd.filter(action="main-menu-balance"))
    dp.register_callback_query_handler(start_payment, menu_cd.filter(action="select-payment"))
    dp.register_pre_checkout_query_handler(process_pre_checkout_query, lambda query: True)
    dp.register_message_handler(got_payment, content_types=ContentTypes.SUCCESSFUL_PAYMENT)
    #dp.register_message_handler(bot_help, CommandHelp())
