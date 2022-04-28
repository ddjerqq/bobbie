from __future__ import annotations
import aiosqlite

from utils import PROJECT_PATH
from database.services.user_service import UserService


class Database:
    _db_path = PROJECT_PATH + "\\database\\database.db"

    def __init__(self):
        self._connection: aiosqlite.Connection | None = None
        self._cursor: aiosqlite.Cursor | None = None
        self.users: UserService | None = None

    async def ainit(self):
        self._connection  = await aiosqlite.connect(self._db_path)
        self._cursor      = await self._connection.cursor()
        self.users = UserService(self._connection, self._cursor)
