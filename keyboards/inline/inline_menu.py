from calendar import c
from data import config
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

        btns.append({'text': 'Ввести вручную номер номенклатуры', "cb": menu_cd.new(action="menu-item-custom", data="void") })
        btns.append({"text": '◀️В меню', 'cb': menu_cd.new(action="main-menu-back", data="void")})
        schema.append(page_schema)
        schema.append(1)
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
    def item_menu(page = 0, item_id = 0, country = 'void'):
        schema = [1, 1]
        btns = [
            {'text': 'Изменить наименование', "cb": changename_cd.new(a="icn", data=item_id, c=country) },
            {'text': '◀️Назад', "cb": menu_cd.new(action="page", data=page) }
        ]
        return InlineMenu._create_kb(btns, schema)

    @staticmethod
    def item_menu_custom(item_id = 0, country = 'void'):
        schema = [1, 1]
        btns = [
            {'text': 'Изменить наименование', "cb": changename_cd.new(a="icn", data=item_id, c=country) },
            {'text': '◀️В меню', "cb": menu_cd.new(action="main-menu-open", data="void") }
        ]
        return InlineMenu._create_kb(btns, schema)

    @staticmethod
    def confirm_country(item_id = 0):
        schema = [1, 1]
        btns = [
            {'text': 'Продолжить', "cb": menu_cd.new(action="country-list", data=item_id) },
            {'text': '◀️В меню', "cb": menu_cd.new(action="main-menu-open", data="void") }
        ]
        return InlineMenu._create_kb(btns, schema)

    @staticmethod
    def country_list_char(item_id = 0):
        schema = [8, 8, 8, 2, 1]
        btns = [
            {'text': 'А', "cb": changename_cd.new(a="scc", data=item_id, c='А') },
            {'text': 'Б', "cb": changename_cd.new(a="scc", data=item_id, c='Б') },
            {'text': 'В', "cb": changename_cd.new(a="scc", data=item_id, c='В') },
            {'text': 'Г', "cb": changename_cd.new(a="scc", data=item_id, c='Г') },
            {'text': 'Д', "cb": changename_cd.new(a="scc", data=item_id, c='Д') },
            {'text': 'Е', "cb": changename_cd.new(a="scc", data=item_id, c='Е') },
            {'text': 'З', "cb": changename_cd.new(a="scc", data=item_id, c='З') },
            {'text': 'И', "cb": changename_cd.new(a="scc", data=item_id, c='И') },
            
            {'text': 'Й', "cb": changename_cd.new(a="scc", data=item_id, c='Й') },
            {'text': 'К', "cb": changename_cd.new(a="scc", data=item_id, c='К') },
            {'text': 'Л', "cb": changename_cd.new(a="scc", data=item_id, c='Л') },
            {'text': 'М', "cb": changename_cd.new(a="scc", data=item_id, c='М') },
            {'text': 'Н', "cb": changename_cd.new(a="scc", data=item_id, c='Н') },
            {'text': 'О', "cb": changename_cd.new(a="scc", data=item_id, c='О') },
            {'text': 'П', "cb": changename_cd.new(a="scc", data=item_id, c='П') },
            {'text': 'Р', "cb": changename_cd.new(a="scc", data=item_id, c='Р') },

            {'text': 'С', "cb": changename_cd.new(a="scc", data=item_id, c='С') },
            {'text': 'Т', "cb": changename_cd.new(a="scc", data=item_id, c='Т') },
            {'text': 'У', "cb": changename_cd.new(a="scc", data=item_id, c='У') },
            {'text': 'Ф', "cb": changename_cd.new(a="scc", data=item_id, c='Ф') },
            {'text': 'Х', "cb": changename_cd.new(a="scc", data=item_id, c='Х') },
            #{'text': 'Ц', "cb": changename_cd.new(a="scc", data=item_id, c='Ц') },
            {'text': 'Ч', "cb": changename_cd.new(a="scc", data=item_id, c='Ч') },
            {'text': 'Ш', "cb": changename_cd.new(a="scc", data=item_id, c='Ш') },
            
            {'text': 'Э', "cb": changename_cd.new(a="scc", data=item_id, c='Э') },
            {'text': 'Ю', "cb": changename_cd.new(a="scc", data=item_id, c='Ю') },
            {'text': 'Я', "cb": changename_cd.new(a="scc", data=item_id, c='Я') },

            {'text': '◀️В меню', "cb": menu_cd.new(action="main-menu-open", data="void") }
        ]
        return InlineMenu._create_kb(btns, schema)

    @staticmethod
    def country_list(country_list: List, item_id = 0):
        schema = []
        btns = []

        for name in country_list:
            if len(name["key"]) > 25: continue

            btns.append({'text': name["key"], "cb": changename_cd.new(a="sc", data=item_id, c=name["key"]) })
            schema.append(1)

        btns.append({'text': '◀️Назад', "cb": menu_cd.new(action="country-list", data=item_id) })
        schema.append(1)
        
        return InlineMenu._create_kb(btns, schema)
        

    @staticmethod
    def select_payment():
        schema = [1]
        btns = []

        for i in range(len(config.prices)):
            btns.append({'text': config.prices[i].label, "cb": menu_cd.new(action="select-payment", data=i) })
            schema.append(1)

        btns.append({'text': '◀️В меню', "cb": menu_cd.new(action="main-menu-open", data="void") })
        return InlineMenu._create_kb(btns, schema)


    @staticmethod
    def payment_button():
        schema = [1, 1]
        btns = [
            {'text': 'Оплатить', "pay": True },
            {'text': '◀️В меню', "cb": menu_cd.new(action="main-menu-open", data="void") }
        ]

        return InlineMenu._create_kb(btns, schema)