from __future__ import annotations
import aiosqlite
import asyncio
import sqlite3

from models.user import User
from utils import *


class Users:
    """
    internal protected subclass for the database
    """
    def __init__(self, cursor: aiosqlite.Cursor):
        self.cursor = cursor

    async def add_user(self, user: User) -> None:
        """
        add user to the database
        :param user: Userobject
        """
        if await self.get_by_id(user.id) is not None:
            return

        await self.cursor.execute("""
        INSERT INTO users
        VALUES(?, ?, ?, ?)
        """, user.to_database)

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

        return User.from_database(tuple(user))

    async def update_name(self, id: int, username: str) -> None:
        """
        update user in the database
        """
        await self.cursor.execute("""
        UPDATE users
        SET username=?
        WHERE id=?
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
        user = await self.get_by_id(id)
        return user is not None


class Database:
    _db_path = os.getcwd() + "\\bobbi.db"

    def __init__(self):
        self.connection: aiosqlite.Connection | None = None
        self.cursor:     aiosqlite.Cursor     | None = None
        self.users:      Users                | None = None

    async def ainit(self) -> None:
        """
        async initor. \n
        `await this to initialize the database`
        """
        rgbprint("[+] database ainit", color="green")
        self.connection = await aiosqlite.connect(self._db_path)
        self.cursor     = await self.connection.cursor()

        self.users      = Users(self.cursor)


    async def save(self):
        await self.connection.commit()


    async def close(self):
        await self.save()
        await asyncio.sleep(1)
        await self.connection.close()
        log("database closed")


database = Database()
