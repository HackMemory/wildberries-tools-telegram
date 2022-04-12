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
from aiogram.types.input_media import *

async def choose_my_items(entity: types.CallbackQuery, callback_data: dict):
    caption = 'Выберете способ'
    kb = keyboards.inline.InlineMenu.before_item_choose()

    if isinstance(entity, types.CallbackQuery):
        await entity.message.edit_text(caption, reply_markup=kb)
        await entity.answer()
        return
    
    await entity.answer(caption, reply_markup=kb)

async def custom_item_id(entity: Union[types.Message, types.CallbackQuery], state: FSMContext):
    caption = 'Введите номер номенкулатуры ниже\nЧтобы отменить действие, напишите /cancel'

    kb = keyboards.inline.InlineMenu.back_menu_button()
    await states.user.user.FindItem.item_id.set()

    if isinstance(entity, types.CallbackQuery):
        await entity.message.edit_text(caption)
        await entity.answer()
        return
    
    await entity.answer(caption)

async def process_custom_item_id(entity: types.Message, state: FSMContext):
    caption = ''
    brend_val = ''
    name_val = ''
    photo_val = ''

    await state.finish()

    has_token = await Users.user_token_exists(entity.from_user.id)

    token = await Users.get_user_token(entity.from_user.id)
    if token == None or token == "":
        return await entity.answer("Произошла ошибка", reply_markup=keyboards.inline.InlineMenu.back_menu_button())

    if not entity.text.isdigit():
        return await entity.answer("Введите верный номер номенкулатуры", reply_markup=keyboards.inline.InlineMenu.back_menu_button())

    data = await wildberries.get_item_info(token, entity.text)
    if data == None:
        return await entity.answer("Произошла ошибка", reply_markup=keyboards.inline.InlineMenu.back_menu_button())

    if len(data["result"]["cards"]) == 0:
        return await entity.answer("Введите верный номер номенкулатуры", reply_markup=keyboards.inline.InlineMenu.back_menu_button())

    card = data["result"]["cards"][0]
    if card == None:
        return await entity.answer("Произошла ошибка", reply_markup=keyboards.inline.InlineMenu.back_menu_button())

    for x in card["addin"]:
        if(x["type"] == "Бренд"): brend_val = x["params"][0]["value"]; break;
    
    for x in card["addin"]:
        if(x["type"] == "Наименование"): name_val = x["params"][0]["value"]; break;

    for x in card["nomenclatures"][0]["addin"]:
        if(x["type"] == "Фото"): photo_val = x["params"][0]["value"]; break;

    kb = keyboards.inline.InlineMenu.item_menu_custom(entity.text)

    nmId = card["nomenclatures"][0]["nmId"]
    caption = f'[{nmId}] [{brend_val}] - {name_val}\n'

    if photo_val:
        photo = InputFile.from_url(photo_val, "media.jpg")
        return await entity.answer_photo(photo, caption=caption, reply_markup=kb)

    await entity.answer(caption, reply_markup=kb)


async def my_items(entity: types.CallbackQuery, callback_data: dict):
    items = []
    page = 0
    caption = 'Ваши товары'

    if callback_data["action"] == "page": page = int(callback_data["data"])

    has_token = await Users.user_token_exists(entity.from_user.id)
    
    token = await Users.get_user_token(entity.from_user.id)
    if token == None or token == "":
        await entity.message.edit_text('Главное меню', reply_markup=keyboards.inline.InlineMenu.main_menu(has_token))
        return await entity.answer("Произошла ошибка")

    data = await wildberries.get_cards_list(token, offset=page*10)
    if data == None:
        await entity.message.edit_text('Главное меню', reply_markup=keyboards.inline.InlineMenu.main_menu(has_token))
        return await entity.answer("Произошла ошибка")

    if isinstance(data, str):
        return await entity.message.edit_text("Произошла ошибка, попробуйте устранить и повторите еще раз\n"+data, reply_markup=keyboards.inline.InlineMenu.back_menu_button())


    total = data["result"]["cursor"]["total"]
    cards = data["result"]["cards"]
    if cards == None:
        await entity.message.edit_text('Главное меню', reply_markup=keyboards.inline.InlineMenu.main_menu(has_token))
        return await entity.answer("Произошла ошибка")

    brend_val = ''
    name_val = ''
    for item in cards:
        for x in item["addin"]:
            if(x["type"] == "Бренд"): brend_val = x["params"][0]["value"]; break;
        
        for x in item["addin"]:
            if(x["type"] == "Наименование"): name_val = x["params"][0]["value"]; break;

        nmId = item["nomenclatures"][0]["nmId"]
        imtId = item["imtId"]
        items.append({"id": nmId, "value": f'[{nmId}] [{brend_val}] - {name_val}'})

    kb = keyboards.inline.InlineMenu.items_list(items, total)
    if callback_data["action"] == "page":
        kb = keyboards.inline.InlineMenu.items_list(items, total, page)

    try:
        await entity.message.edit_text(caption, reply_markup=kb)
        await entity.answer()
    except:
        await entity.message.answer(caption, reply_markup=kb)


async def select_item(entity: types.CallbackQuery, callback_data: dict):
    caption = ''
    brend_val = ''
    name_val = ''
    photo_val = ''

    has_token = await Users.user_token_exists(entity.from_user.id)

    kb = keyboards.inline.InlineMenu.main_menu(has_token)

    token = await Users.get_user_token(entity.from_user.id)
    if token == None or token == "":
        return await entity.answer('Произошла ошибка', reply_markup=kb)

    data = await wildberries.get_item_info(token, callback_data["data"])
    if data == None:
        return await entity.answer('Произошла ошибка', reply_markup=kb)

    card = data["result"]["cards"][0]
    if card == None:
        return await entity.answer('Произошла ошибка', reply_markup=kb)

    for x in card["addin"]:
        if(x["type"] == "Бренд"): brend_val = x["params"][0]["value"]; break;
    
    for x in card["addin"]:
        if(x["type"] == "Наименование"): name_val = x["params"][0]["value"]; break;

    for x in card["nomenclatures"][0]["addin"]:
        if(x["type"] == "Фото"): photo_val = x["params"][0]["value"]; break;


    kb = keyboards.inline.InlineMenu.item_menu(callback_data["page"], callback_data["data"])
    nmId = card["nomenclatures"][0]["nmId"]
    caption = f'[{nmId}] [{brend_val}] - {name_val}\n'

    if photo_val:
        photo = InputFile.from_url(photo_val, "media.jpg")
        return await entity.message.answer_photo(photo, caption=caption, reply_markup=kb)

    await entity.message.answer(caption, reply_markup=kb)


async def select_country_char(entity: types.CallbackQuery, callback_data: dict):
    caption = 'Выберите страну'
    kb = keyboards.inline.InlineMenu.country_list_char(callback_data["data"])

    if isinstance(entity, types.CallbackQuery):
        await entity.message.edit_text(caption, reply_markup=kb)
        await entity.answer()
        return
    
    await entity.answer(caption, reply_markup=kb)

async def select_country_list(entity: types.CallbackQuery, callback_data: dict):
    caption = 'Выберите страну'

    token = await Users.get_user_token(entity.from_user.id)
    if token == None or token == "":
        return await entity.answer("Произошла ошибка", reply_markup=keyboards.inline.InlineMenu.back_menu_button())

    list = await wildberries.country_list(token, callback_data["c"])
    kb = keyboards.inline.InlineMenu.country_list(list, callback_data["data"])

    if isinstance(entity, types.CallbackQuery):
        await entity.message.edit_text(caption, reply_markup=kb)
        await entity.answer()
        return
    
    await entity.answer(caption, reply_markup=kb)



async def change_name(entity: types.CallbackQuery, callback_data: dict, state: FSMContext):
    caption = 'Введите наименование (не большо 100 символов)\nЧтобы отменить действие, напишите /cancel'

    token = await Users.get_user_token(entity.from_user.id)
    if token == None or token == "":
        return await entity.answer("Произошла ошибка", reply_markup=keyboards.inline.InlineMenu.back_menu_button())

    data = await wildberries.get_item_info(token, callback_data["data"])
    if data == None:
        return await entity.answer('Произошла ошибка', reply_markup=kb)

    card = data["result"]["cards"][0]
    if card == None:
        return await entity.answer('Произошла ошибка', reply_markup=kb)

    if card['countryProduction'] == '' and callback_data["c"] == 'void': 
        return await entity.message.answer(
            'У вас не указана страна производителя, без этого не изменить наименование. Укажите, чтобы продолжить...',
            reply_markup=keyboards.inline.InlineMenu.confirm_country(callback_data["data"])
        )


    kb = keyboards.inline.InlineMenu.back_menu_button()
    await states.user.user.ChangeItem.item_name.set()
    async with state.proxy() as data:
        data['item_id'] = callback_data["data"]
        data['country'] = callback_data["c"]

    if isinstance(entity, types.CallbackQuery):
        await entity.message.answer(caption)
        return
    
    await entity.answer(caption)

async def process_change_name(entity: types.Message, state: FSMContext):
    if len(entity.text) > 100:
        return await entity.answer('Наименование превышеает 100 символов')

    has_token = await Users.user_token_exists(entity.from_user.id)

    token = await Users.get_user_token(entity.from_user.id)
    if token == None or token == "":
        await state.finish()
        return await entity.answer("Произошла ошибка", reply_markup=keyboards.inline.InlineMenu.back_menu_button())

    
    state_data = await state.get_data()
    data = await wildberries.change_item_name(token, state_data["item_id"], entity.text, state_data["country"])
    if data == None:
        await state.finish()
        return await entity.answer("Произошла ошибка", reply_markup=keyboards.inline.InlineMenu.back_menu_button())

    if isinstance(data, str):
        await state.finish()
        return await entity.answer("Произошла ошибка, попробуйте устранить и повторите еще раз\n"+data, reply_markup=keyboards.inline.InlineMenu.back_menu_button())

    await state.finish()

    kb = keyboards.inline.InlineMenu.back_menu_button()
    await entity.answer("Наименование успешно изменено", reply_markup=kb)