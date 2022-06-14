import aiosqlite

from database.factories.pet_factory import PetFactory
from database.models.pet import Pet


class PetRepository:
    """
    it's your responsibility to commit the changes to the database
    """
    def __init__(self, connection: aiosqlite.Connection, cursor: aiosqlite.Cursor):
        self._connection = connection
        self._cursor     = cursor

    async def save_changes(self):
        await self._connection.commit()

    async def get_all(self) -> list[Pet | None]:
        await self._cursor.execute("""
        SELECT * FROM pets;
        """)
        rows = await self._cursor.fetchall()
        return [PetFactory.from_db_row(row) for row in rows]

    async def get(self, id: int) -> Pet | None:
        await self._cursor.execute("""
        SELECT * FROM pets 
        WHERE id=?;
        """, (id,))
        data = await self._cursor.fetchone()
        if data is not None:
            data = PetFactory.from_db_row(data)
        return data

    async def add(self, entity: Pet) -> None:
        await self._cursor.execute("""
        INSERT OR IGNORE INTO pets
        (
            id,
            type,
            rarity,
            level,
            owner_id
        )
        VALUES
        (
            :id, 
            :type,
            :rarity, 
            :level,
            :owner_id
        );
        """, entity.db_dict)

    async def update(self, entity: Pet) -> None:
        await self._cursor.execute("""
        UPDATE pets 
        SET 
            type=:type,
            rarity=:rarity,
            level=:level,
            owner_id=:owner_id
        WHERE id=:id;
        """, entity.db_dict)

    async def delete(self, entity: Pet) -> None:
        await self._cursor.execute("""
        DELETE FROM pets
        WHERE id=:id;
        """, entity.db_dict)
