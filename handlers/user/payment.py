from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext
from data import config

import keyboards.inline
from services import wildberries
from states.user import user
from utils.db.db_api.users import Users

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
        payload='wildberries-payment',
        reply_markup=kb
    )


async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True, error_message="По какой-то причине платеж не прошел. Попробуйте позже еще раз.")


async def got_payment(entity: types.Message):
    kb = keyboards.inline.InlineMenu.back_menu_button()
    entity.answer("Спасибо за покупку!", reply_markup=kb)
