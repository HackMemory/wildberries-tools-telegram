from .storages import SqliteConnection

class Users(SqliteConnection):
    async def create_table_users(self):
        sql = """
        CREATE TABLE Users (
            id int NOT NULL,
            name varchar(255),
            token varchar(255),
            phone varchar(255),
            PRIMARY KEY (id)
            );
"""
        await self.__make_request(sql)

    @staticmethod
    async def add_user(id: int, name: str, phone: str = None):

        sql = """
        INSERT INTO Users(id, name, phone) VALUES(%s, %s, %s)
        """
        await Users.__make_request(sql, params=(id, name, phone))

    @staticmethod
    async def select_all_users():
        sql = """
        SELECT * FROM Users
        """
        return await Users.__make_request(sql, fetch=True, mult=True)

    @staticmethod
    async def count_users():
        return await Users.__make_request("SELECT COUNT(*) FROM Users;", fetch=True)

    @staticmethod
    async def update_user_token(token, id):
        # SQL_EXAMPLE = "UPDATE Users SET token=##### WHERE id=12345"

        sql = f"""
        UPDATE Users SET token=%s WHERE id=%s
        """
        await Users.__make_request(sql, params=(token, id))

    @staticmethod
    async def update_user_phone(phone, id):
        # SQL_EXAMPLE = "UPDATE Users SET phone=##### WHERE id=12345"

        sql = f"""
        UPDATE Users SET phone=%s WHERE id=%s
        """
        await Users.__make_request(sql, params=(phone, id))

    @staticmethod
    async def delete_users():
        await Users.__make_request("DELETE FROM Users WHERE TRUE")
