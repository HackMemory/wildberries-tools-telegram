from .storages import SqliteConnection
from data import config

class Users(SqliteConnection):
    @staticmethod
    async def create_table_users():
        sql = """
        CREATE TABLE Users (
            id int NOT NULL,
            name varchar(255),
            token varchar(255),
            phone varchar(255),
            change_count int,
            PRIMARY KEY (id)
            );
"""
        Users._make_request(sql)

    @staticmethod
    async def add_user(id: int, name: str, phone: str = None):

        sql = f"""
        INSERT INTO Users(id, name, phone, change_count) VALUES(?, ?, ?, ?)
        """
        Users._make_request(sql, params=(id, name, phone, config.FREE_CHANGE_COUNT))

    @staticmethod
    async def select_all_users():
        sql = """
        SELECT * FROM Users
        """
        return Users._make_request(sql, fetch=True, mult=True)

    @staticmethod
    async def count_users():
        return Users._make_request("SELECT COUNT(*) FROM Users;", fetch=True)

    @staticmethod
    async def user_token_exists(id):
        sql = f"""
        SELECT * from Users WHERE id=?
        """

        row = Users._make_request(sql, params=(id,),fetch=True, mult=False)
        if row != None:
            token = row["token"]
            if token == None or token == "":
                return False
            else:
                return True

    @staticmethod
    async def get_user_token(id):
        sql = f"""
        SELECT * from Users WHERE id=?
        """

        row = Users._make_request(sql, params=(id,),fetch=True, mult=False)
        if row != None:
            token = row["token"]
            return token
        
        return None

    @staticmethod
    async def get_user_count(id):
        sql = f"""
        SELECT * from Users WHERE id=?
        """

        row = Users._make_request(sql, params=(id,),fetch=True, mult=False)
        if row != None:
            count = row["change_count"]
            return count
        
        return None

    @staticmethod
    async def update_user_token(token, id):
        # SQL_EXAMPLE = "UPDATE Users SET token=##### WHERE id=12345"

        sql = f"""
        UPDATE Users SET token=? WHERE id=?
        """
        Users._make_request(sql, params=(token, id))

    @staticmethod
    async def update_user_phone(phone, id):
        # SQL_EXAMPLE = "UPDATE Users SET phone=##### WHERE id=12345"

        sql = f"""
        UPDATE Users SET phone=? WHERE id=?
        """
        Users._make_request(sql, params=(phone, id))

    @staticmethod
    async def delete_users():
        Users._make_request("DELETE FROM Users WHERE TRUE")
