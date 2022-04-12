from contextlib import suppress
from typing import Union

from aiogram import types
from aiogram.dispatcher import FSMContext

import keyboards.inline
from services import wildberries
from states.user import user
from utils.db.db_api.users import Users


async def cancel_handler(message: types.Message, state: FSMContext):
    kb = keyboards.inline.InlineMenu.back_menu_button()
    current_state = await state.get_state()
    if current_state is None:
        return
    # Cancel state and inform user about it
    await state.finish()
    # And remove keyboard (just in case)
    await message.answer('Действие отменено.', reply_markup=kb)


async def bot_start(entity: types.Message, state: FSMContext):
    caption = f'Тут какой-то приветсвенный текст'
    kb = keyboards.inline.InlineMenu.start_menu()
    
    if not entity.from_user.is_bot:
        await Users.add_user(entity.from_user.id, entity.from_user.full_name)
    await entity.answer(caption, reply_markup=kb)


async def main_menu(entity: Union[types.Message, types.CallbackQuery], state: FSMContext):
    caption = f'Главное меню'
    has_token = await Users.user_token_exists(entity.from_user.id)

    kb = keyboards.inline.InlineMenu.main_menu(has_token)

    if isinstance(entity, types.CallbackQuery):
        try:
            await entity.message.edit_text(caption, reply_markup=kb)
            await entity.answer()
            return
        except:
            return await entity.message.answer(caption, reply_markup=kb)
    
    await entity.answer(caption, reply_markup=kb)



async def remove_token_confirm(entity: Union[types.Message, types.CallbackQuery], state: FSMContext):
    caption = f'Токен удален'

    kb = keyboards.inline.InlineMenu.back_menu_button()
    await Users.update_user_token("", entity.from_user.id)

    if isinstance(entity, types.CallbackQuery):
        await entity.message.edit_text(caption, reply_markup=kb)
        await entity.answer()
        return
    
    await entity.answer(caption, reply_markup=kb)


async def remove_token(entity: Union[types.Message, types.CallbackQuery], state: FSMContext):
    caption = f'Вы уверены?'
    kb = keyboards.inline.InlineMenu.token_confirm()

    if isinstance(entity, types.CallbackQuery):
        await entity.message.edit_text(caption, reply_markup=kb)
        await entity.answer()
        return
    
    await entity.answer(caption, reply_markup=kb)

async def add_token(entity: Union[types.Message, types.CallbackQuery], state: FSMContext):
    caption = "Введите ваш токен ниже\nЧтобы отменить действие, напишите /cancel"

    kb = keyboards.inline.InlineMenu.back_menu_button()
    await user.Token.token.set()

    if isinstance(entity, types.CallbackQuery):
        await entity.message.edit_text(caption)
        await entity.answer()
        return
    
    await entity.answer(caption)

async def process_token(entity: types.Message, state: FSMContext):
    kb = keyboards.inline.InlineMenu.back_menu_button()
    if await wildberries.validate_token(entity.text):
        await Users.update_user_token(entity.text, entity.from_user.id)
        await entity.answer("Успех! Ваш токен валидный. Вернитесь в меню и начните пользоваться ботом.", reply_markup=kb)
    else:
        await entity.answer("Невадлиный токен! Вернитесь и попробуйте еще раз.", reply_markup=kb)
    
    await state.finish()


async def profile(entity: Union[types.Message, types.CallbackQuery], state: FSMContext):
    count = await Users.get_user_count(entity.from_user.id)
    kb = keyboards.inline.InlineMenu.back_menu_button()

    caption = 'Тут какой-то текст мб в профиле\n'
    caption += f'Доступное количество изменений: {count}'

    if isinstance(entity, types.CallbackQuery):
        await entity.message.edit_text(caption, reply_markup=kb)
        await entity.answer()
        return

    await entity.answer(caption, reply_markup=kb)