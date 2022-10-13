import asyncio

import aiosqlite

from database.factories.marriage_factory import MarriageFactory
from database.models.marriage import Marriage


class MarriageRepository:
    """
    it's your responsibility to commit the changes to the database
    """
    def __init__(self, connection: aiosqlite.Connection, cursor: aiosqlite.Cursor):
        self._connection = connection
        self._cursor     = cursor

    async def save_changes(self):
        await self._connection.commit()

    async def get_all(self) -> list[Marriage]:
        await self._cursor.execute("""
        SELECT * FROM marriages;
        """)
        rows = await self._cursor.fetchall()
        return [MarriageFactory.from_db_row(row) for row in rows]

    async def get(self, id: int) -> Marriage | None:
        await self._cursor.execute("""
        SELECT * FROM marriages
        WHERE id=?;
        """, (id,))
        row = await self._cursor.fetchone()
        if row is None:
            return None
        return MarriageFactory.from_db_row(row)

    async def add(self, entity: Marriage) -> None:
        await self._cursor.execute("""
        INSERT OR IGNORE INTO marriages
        (
            id,
            king_id,
            bride_id,
            guild_id,
            bride_role_id,
            king_role_id
        )
        VALUES
        (
            :id, 
            :king_id,
            :bride_id,
            :guild_id,
            :bride_role_id,
            :king_role_id
        );
        """, entity.db_dict)

    async def update(self, entity: Marriage) -> None:
        await self._cursor.execute("""
        UPDATE marriages
        SET 
            king_id=:king_id,
            bride_id=:bride_id,
            guild_id=:guild_id,
            bride_role_id=:bride_role_id,
            king_role_id=:king_role_id            
        WHERE id=:id;
        """, entity.db_dict)

    async def delete(self, entity: Marriage) -> None:
        await self._cursor.execute("""
        DELETE FROM marriages
        WHERE id=:id;
        """, entity.db_dict)
