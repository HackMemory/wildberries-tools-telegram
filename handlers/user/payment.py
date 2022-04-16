from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from data import config

import keyboards.inline
from services import wildberries
from states.user import user
from utils.db.db_api.payments import Payments
from utils.db.db_api.users import *

async def select_payment(entity: types.CallbackQuery, state: FSMContext):
    caption = 'Тут какой-то текст про оплату'

    kb = keyboards.inline.InlineMenu.select_payment()
    await entity.message.edit_text(caption, reply_markup=kb)

async def start_payment(entity: types.CallbackQuery, state: FSMContext, callback_data: dict):
    kb = keyboards.inline.InlineMenu.payment_button()
    index = callback_data["data"]
    await entity.bot.send_invoice(
        entity.message.chat.id,
        title='Изменение карточек Wildberries',
        description='Какое то общее описание для всех платежей',
        provider_token=config.PAYMENTS_PROVIDER_TOKEN,
        currency='rub',
        is_flexible=False,
        prices=[config.prices[int(index)]],
        start_parameter='wildberries-payment-0000',
        payload=index,
        reply_markup=kb
    )


async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True, error_message="По какой-то причине платеж не прошел. Попробуйте позже еще раз.")


async def got_payment(entity: types.Message):
    kb = keyboards.inline.InlineMenu.back_menu_button()

    sp = entity.successful_payment
    index = int(sp.invoice_payload)
    
    await Users.add_user_change_count(entity.from_user.id, config.prices_amount[index])
    await Payments.add_payment(entity.from_user.id, entity.from_user.username, sp.telegram_payment_charge_id, sp.provider_payment_charge_id, sp.total_amount//100)

    await entity.answer("Спасибо за покупку!", reply_markup=kb)
