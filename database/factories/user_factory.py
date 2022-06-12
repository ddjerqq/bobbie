import sqlite3
from database.models.user import User


class UserFactory:
    @classmethod
    def new(cls, snowflake: int, username: str) -> User:
        """
        create a new user and set its values to the defaults
        """
        return User(snowflake, username, 0, 0, 0)

    @classmethod
    def from_db_row(cls, data: sqlite3.Row) -> User:
        data = dict(data)

        id = data.pop("snowflake")
        username = data.pop("username")
        experience = data.pop("experience")
        bank = data.pop("bank")
        wallet = data.pop("wallet")

        return User(id, username, experience, bank, wallet)
