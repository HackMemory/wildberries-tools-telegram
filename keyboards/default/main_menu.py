from .consts import DefaultConstructor
from typing import List


class MainMenu(DefaultConstructor):
    @staticmethod
    def main_menu():
        schema = [3]
        actions = [
            '➕Добавить токен',
            '📖Мои товары',
            '💳Пополнить баланс'
        ]
        return MainMenu._create_kb(actions, schema)