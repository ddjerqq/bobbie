from __future__ import annotations
import aiosqlite

from utils import PROJECT_PATH
from services.user_service import UserService
from services.item_service import ItemService


class Database:
    _db_path = PROJECT_PATH + "/database.db"

    def __init__(self):
        self._connection: aiosqlite.Connection | None = None
        self._cursor: aiosqlite.Cursor | None = None
        self.user_service: UserService | None = None
        self.item_service: ItemService | None = None

    async def ainit(self):
        self._connection = await aiosqlite.connect(self._db_path)
        self._cursor     = await self._connection.cursor()

        self.user_service = UserService(self._connection, self._cursor)
        self.item_service = ItemService(self._connection, self._cursor)

        await self._regenerate_tables()

    async def _regenerate_tables(self):
        # users
        await self._cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users
        (
            snowflake  INTEGER      NOT NULL
                CONSTRAINT users_pk
                    PRIMARY KEY,
            username   NVARCHAR(50) NOT NULL,
            experience INTEGER NOT NULL DEFAULT 0,
            wallet     INTEGER NOT NULL DEFAULT 0,
            bank       INTEGER NOT NULL DEFAULT 0
        );

        -- index snowflake
        CREATE UNIQUE INDEX IF NOT EXISTS 
        users_snowflake_uindex 
        ON users (snowflake);
        """)

        # items
        await self._cursor.executescript("""
        CREATE TABLE IF NOT EXISTS items
        (
            id       INTEGER     NOT NULL 
                CONSTRAINT items_pk PRIMARY KEY,
            type     VARCHAR(32) NOT NULL,
            rarity   REAL        NOT NULL,
            owner_id INTEGER     DEFAULT NULL
                CONSTRAINT items_users_snowflake_fk
                    REFERENCES users
        );
        
        CREATE UNIQUE INDEX IF NOT EXISTS 
        items_id_uindex
        ON items (id);
        """)

    async def close(self):
        await self._connection.commit()
        await self._connection.close()
