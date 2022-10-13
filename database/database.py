from __future__ import annotations

import aiosqlite

from database.services.marriage_service import MarriageService
from database.services.user_service import UserService


class Database:
    def __init__(self, connection: aiosqlite.Connection, cursor: aiosqlite.Cursor):
        self._connection = connection
        self._cursor     = cursor
        self.users       = UserService(connection, cursor)
        self.marriages   = MarriageService(connection, cursor)

    @classmethod
    async def ainit(cls, path: str) -> Database:
        connection = await aiosqlite.connect(path)
        cursor     = await connection.cursor()
        return cls(connection, cursor)
