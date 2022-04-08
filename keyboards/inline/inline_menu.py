from .consts import InlineConstructor
from typing import List
from .callbacks import *

class InlineMenu(InlineConstructor):

    @staticmethod
    def back_menu_button():
        schema = [1]
        btns = [
            {'text': '◀️В меню', "cb": menu_cd.new(action="main-menu-open", data="void") }
        ]
        return InlineMenu._create_kb(btns, schema)

    @staticmethod
    def start_menu():
        schema = [1]
        btns = [
            {'text': '🎛️Открыть меню', "cb": menu_cd.new(action="main-menu-open", data="void") }
        ]
        return InlineMenu._create_kb(btns, schema)

    @staticmethod
    def main_menu(has_token: bool):
        btns = []
        schema = [1, 1]

        if has_token: 
            btns.append({'text': '❌Удалить токен', "cb": menu_cd.new(action="main-menu-remove-token", data="void") })
            btns.append({'text': '📖Мои товары', "cb": menu_cd.new(action="main-menu-items", data="void")})
            schema.append(1)
            schema.append(1)
        else:
            btns.append({'text': '➕Добавить токен', "cb": menu_cd.new(action="main-menu-add-token", data="void") })
            schema.append(1)

        btns.append({'text': '👤Мой профиль', "cb": menu_cd.new(action="main-menu-profile", data="void")})
        btns.append({'text': '💳Пополнить баланс', "cb": menu_cd.new(action="main-menu-balance", data="void")})

        return InlineMenu._create_kb(btns, schema)

    @staticmethod
    def items_list(items: List, total_count, page = 0, per_page = 10):
        schema = []
        btns = []

        has_next_page = (total_count//per_page) + 1 > int(page) + 1

        for i in range(0, len(items)):     
            btns.append({"text": items[i]["value"], 'cb': item_cd.new(action="select-item", data=items[i]["id"], page=page)})
            schema.append(1)

        page_schema = 0
        if page != 0:
            btns.append({"text": '⬅️', 'cb': menu_cd.new(action="page", data=page-1)})
            page_schema += 1

        if has_next_page:
            btns.append({"text": '➡️', 'cb': menu_cd.new(action="page", data=page+1)})
            page_schema += 1

        btns.append({"text": '◀️В меню', 'cb': menu_cd.new(action="main-menu-back", data="void")})
        schema.append(page_schema)
        schema.append(1)

        return InlineMenu._create_kb(btns, schema)

    @staticmethod
    def token_confirm():
        schema = [2]
        btns = [
            {'text': '✅Да', "cb": menu_cd.new(action="token-yes", data="void") },
            {'text': '❌Нет', "cb": menu_cd.new(action="main-menu-back", data="void") },
        ]
        return InlineMenu._create_kb(btns, schema)


    @staticmethod
    def before_item_choose():
        schema = [1, 1, 1]
        btns = [
            {'text': 'Выбрать из списка', "cb": menu_cd.new(action="menu-items-choose", data="void") },
            {'text': 'Ввести вручную номер номенклатуры', "cb": menu_cd.new(action="menu-item-custom", data="void") },
            {'text': '◀️В меню', "cb": menu_cd.new(action="main-menu-open", data="void") }
        ]
        return InlineMenu._create_kb(btns, schema)


    @staticmethod
    def item_menu(page = 0):
        schema = [1, 1]
        btns = [
            {'text': 'Изменить наименование', "cb": menu_cd.new(action="item-change-name", data="void") },
            {'text': '◀️Назад', "cb": menu_cd.new(action="page", data=page) }
        ]
        return InlineMenu._create_kb(btns, schema)

    @staticmethod
    def item_menu_custom():
        schema = [1, 1]
        btns = [
            {'text': 'Изменить наименование', "cb": menu_cd.new(action="item-change-name", data="void") },
            {'text': '◀️В меню', "cb": menu_cd.new(action="main-menu-open", data="void") }
        ]
        return InlineMenu._create_kb(btns, schema)