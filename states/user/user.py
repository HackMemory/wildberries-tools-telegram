from aiogram.dispatcher.filters.state import State, StatesGroup

class Token(StatesGroup):
    token = State()

class ChangeItem(StatesGroup):
    item_name = State()
    item_id = State()
    country = State()

class FindItem(StatesGroup):
    item_id = State()

