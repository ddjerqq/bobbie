from __future__ import annotations

import random

import aiosqlite

from database.services.user_service import UserService


class Database:
    def __init__(self, connection: aiosqlite.Connection, cursor: aiosqlite.Cursor):
        self._connection = connection
        self._cursor     = cursor
        self.users       = UserService(connection, cursor)


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

    @classmethod
    async def ainit(cls, path: str):
        connection  = await aiosqlite.connect(path)
        cursor      = await connection.cursor()
        return cls(connection, cursor)
