from __future__ import annotations
import aiosqlite
import asyncio
import sqlite3

from models.database.dbusers import DbUsers
from utils import *



class Database:
    _db_path = os.getcwd() + "\\bobbi.db"

    def __init__(self):
        self.connection: aiosqlite.Connection | None = None
        self.cursor:     aiosqlite.Cursor     | None = None
        self.users:      DbUsers                | None = None


    async def ainit(self) -> None:
        """
        async initor. \n
        `await this to initialize the database`
        """
        rgbprint("[+] database ainit", color="green")
        self.connection = await aiosqlite.connect(self._db_path)
        self.cursor     = await self.connection.cursor()
        self.users      = DbUsers(self.cursor)

        await self._regenerate_tables()


    async def _regenerate_tables(self):
        # user table
        await self.cursor.executescript("""
        CREATE TABLE IF NOT EXISTS users
        (
            snowflake  INTEGER      NOT NULL
                CONSTRAINT users_pk
                    PRIMARY KEY,
            username   NVARCHAR(50) NOT NULL,
            joindate   DATE,
            experience INTEGER DEFAULT 0,
            wallet     INTEGER NOT NULL DEFAULT 0,
            bank       INTEGER NOT NULL DEFAULT 0
        );
        
        -- index snowflake
        CREATE UNIQUE INDEX IF NOT EXISTS 
        users_snowflake_uindex 
        ON users (snowflake);
        """)


    async def save(self):
        await self.connection.commit()


    async def close(self):
        await self.save()
        await self.connection.close()
        log("database closed")


database = Database()
