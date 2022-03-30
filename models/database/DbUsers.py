from __future__ import annotations
import aiosqlite

from models.user import User
from utils import *


class DbUsers:
    """
    internal protected subclass for the database
    """
    def __init__(self, cursor: aiosqlite.Cursor):
        self.cursor = cursor


    async def get_by_id(self, id: int) -> User | None:
        """
        get the user by id
        :param id: snowflake id
        :return: None or the user object
        """
        await self.cursor.execute("""
        SELECT * FROM users
        WHERE snowflake=?
        """, (id,))
        user = await self.cursor.fetchone()

        if not user:
            return None

        # DEBUG
        print("user inside get_by_id", user)

        return User.from_database(tuple(user))


    async def add_user(self, user: User) -> None:
        """
        add user to the database
        :param user: Userobject
        """
        if await self.get_by_id(user.id) is not None:
            return

        await self.cursor.execute("""
        INSERT INTO users
        VALUES(?, ?, ?, ?, ?, ?)
        """, user.to_database)


    async def update_name(self, id: int, username: str) -> None:
        """
        update user in the database
        """
        await self.cursor.execute("""
        UPDATE users
        SET username=?
        WHERE snowflake=?
        """, (username, id))


    async def add_experience(self, id: int, xp_amount: int) -> None:
        """
        add xp to user IF USER EXISTS
        :param id:
        :param xp_amount: int amount of xp
        """
        await self.cursor.execute("""
        UPDATE users
        SET experience=experience+?
        WHERE snowflake=?
        """, (xp_amount, id))


    async def exists(self, id: int) -> bool:
        """
        check if a user is registered
        """
        await self.cursor.execute("""
        SELECT username FROM users
        WHERE snowflake=?
        """, (id,))
        r = await self.cursor.fetchone()
        return r is not None


    async def get_user_balance(self, user_id: int) -> tuple[int, int] | None:
        """
        get the tuple(bank, wallet) of a user
        make sure user exists
        :return: may be None
        """
        await self.cursor.execute("""
        SELECT bank, wallet FROM users
        WHERE snowflake=?
        """, (user_id,))
        r = await self.cursor.fetchone()
        if r is not None:
            bank, wallet = r
            return bank, wallet
        else:
            return None


    async def wallet(self, user_id: int, amount: int) -> None:
        """
        change amount of wallet for user \n
        THIS DOES NOT TAKE INTO ACCOUNT UNSIGNED VALUES
        CHECK SOMEWHERE ELSE FOR NEGATIVES!!!!!!!!!!!!!
        """
        await self.cursor.execute("""
        UPDATE users 
        SET wallet=wallet+?
        WHERE snowflake=?
        """, (amount, user_id))


    async def bank(self, user_id: int, amount: int) -> None:
        """
        change amount of bank for user \n
        THIS DOES NOT TAKE INTO ACCOUNT UNSIGNED VALUES
        CHECK SOMEWHERE ELSE FOR NEGATIVES!!!!!!!!!!!!!
        """
        await self.cursor.execute("""
        UPDATE users 
        SET bank=bank+?
        WHERE snowflake=?
        """, (amount, user_id))
