from .storages import SqliteConnection
from data import config

class Payments(SqliteConnection):
    @staticmethod
    async def create_table_payments():
        sql = """
        CREATE TABLE Payments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id int NOT NULL,
            telegram_name varchar(255),
            telegram_payment_charge_id varchar(255),
            provider_payment_charge_id varchar(255),
            total_amount int
            );
"""
        Payments._make_request(sql)

    @staticmethod
    async def add_payment(tg_id: int, username: str, telegram_payment_charge_id: str, provider_payment_charge_id: str, total_amount: int):

        sql = f"""
        INSERT INTO Payments(telegram_id, telegram_name, telegram_payment_charge_id, provider_payment_charge_id, total_amount) VALUES(?, ?, ?, ?, ?)
        """
        Payments._make_request(sql, params=(tg_id, username, telegram_payment_charge_id, provider_payment_charge_id, total_amount))