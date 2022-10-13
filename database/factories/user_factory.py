import sqlite3
from database.models.user import User


class UserFactory:
    @classmethod
    def new(cls, snowflake: int, username: str) -> User:
        """
        create a new user and set its values to the defaults
        """
        return User(snowflake, username, 0, 0, 0, None)

    @classmethod
    def from_db_row(cls, data: tuple[int, str, int, int, int, int]) -> User:
        return User(*data)
