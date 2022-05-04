from __future__ import annotations

import random

import aiosqlite

from database.services.user_service import UserService


class Database:
    _db_path = "database/database.db"

    def __init__(self):
        self._connection: aiosqlite.Connection | None = None
        self._cursor: aiosqlite.Cursor | None = None
        self.users: UserService | None = None


    async def verify_word(self, word: str, status: int):
        """
        verify word in database \n
        :param str word:
        :param int status: if valid 1, else 0
        """
        await self._cursor.execute("""
        UPDATE words
        SET verified=?
        WHERE word=?
        """, (status, word))

    async def unverified_word(self):
        await self._cursor.execute("""
        SELECT * FROM words
        WHERE verified IS NULL OR verified=0
        """)
        words = await self._cursor.fetchall()
        return random.choice(list(words))


    async def ainit(self):
        self._connection  = await aiosqlite.connect(self._db_path)
        self._cursor      = await self._connection.cursor()
        self.users = UserService(self._connection, self._cursor)
