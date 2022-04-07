from contextlib import suppress
from data import config

from aiogram import types
from aiogram.dispatcher import FSMContext

from keyboards import *
import keyboards
from typing import Union
import states.user
from services import wildberries
from utils.db.db_api.users import Users

async def choose_my_items(entity: types.CallbackQuery, callback_data: dict):
    caption = 'Выберете способ'
    kb = keyboards.inline.InlineMenu.before_item_choose()

    if isinstance(entity, types.CallbackQuery):
        await entity.message.edit_text(caption, reply_markup=kb)
        await entity.answer()
        return
    
    await entity.answer(caption, reply_markup=kb)

async def custom_item_id(entity: Union[types.Message, types.CallbackQuery], state: FSMContext):
    caption = 'Введите номер номенкулатуры ниже'

    kb = keyboards.inline.InlineMenu.back_menu_button()
    await states.user.user.FindItem.item_id.set()

    if isinstance(entity, types.CallbackQuery):
        await entity.message.edit_text(caption)
        await entity.answer()
        return
    
    await entity.answer(caption)

async def process_custom_item_id(entity: types.Message, state: FSMContext):
    kb = keyboards.inline.InlineMenu.back_menu_button()
    # if await wildberries.validate_token(entity.text):
    #     await Users.update_user_token(entity.text, entity.from_user.id)
    #     await entity.answer("Успех! Ваш токен валидный. Вернитесь в меню и начните пользоваться ботом.", reply_markup=kb)
    # else:
    #     await entity.answer("Невадлиный токен! Вернитесь и попробуйте еще раз.", reply_markup=kb)

    await entity.answer("Тест" + entity.text, reply_markup=kb)
    await state.finish()

async def my_items(entity: types.CallbackQuery, callback_data: dict):
    items = []
    page = 0
    caption = 'Ваши товары'

    if callback_data["action"] == "page": page = int(callback_data["data"])
    
    token = await Users.get_user_token(entity.from_user.id)
    if token == None or token == "":
        await entity.message.edit_text('Главное меню', reply_markup=keyboards.inline.InlineMenu.main_menu())
        return await entity.answer("Произошла ошибка")

    data = await wildberries.get_cards_list(token, offset=page*10)
    if data == None:
        await entity.message.edit_text('Главное меню', reply_markup=keyboards.inline.InlineMenu.main_menu())
        return await entity.answer("Произошла ошибка")

    total = data["result"]["cursor"]["total"]
    cards = data["result"]["cards"]
    if cards == None:
        await entity.message.edit_text('Главное меню', reply_markup=keyboards.inline.InlineMenu.main_menu())
        return await entity.answer("Произошла ошибка")

    brend_val = ''
    name_val = ''
    for item in cards:
        for x in item["addin"]:
            if(x["type"] == "Бренд"): brend_val = x["params"][0]["value"]; break;
        
        for x in item["addin"]:
            if(x["type"] == "Наименование"): name_val = x["params"][0]["value"]; break;

        nmId = item["nomenclatures"][0]["nmId"]
        items.append({"id": nmId, "value": f'[{nmId}] [{brend_val}] - {name_val}'})

    kb = keyboards.inline.InlineMenu.items_list(items, total)
    if callback_data["action"] == "page":
        kb = keyboards.inline.InlineMenu.items_list(items, total, page)

    await entity.message.edit_text(caption, reply_markup=kb)
    await entity.answer()
