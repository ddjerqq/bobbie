import aiosqlite

from database.factories.item_factory import ItemFactory
from database.models.item import Item


class ItemRepository:
    """
    it's your responsibility to commit the changes to the database
    """
    def __init__(self, connection: aiosqlite.Connection, cursor: aiosqlite.Cursor):
        self._connection = connection
        self._cursor     = cursor

    async def save_changes(self):
        await self._connection.commit()

    async def get_all(self) -> list[Item | None]:
        await self._cursor.execute("""
        SELECT * FROM items;
        """)
        rows = await self._cursor.fetchall()
        return [ItemFactory.from_db_row(row) for row in rows]

    async def get(self, id: int) -> Item | None:
        await self._cursor.execute("""
        SELECT * FROM items 
        WHERE id=?;
        """, (id,))
        data = await self._cursor.fetchone()
        if data is not None:
            data = ItemFactory.from_db_row(data)
        return data

    async def add(self, item: Item) -> None:
        await self._cursor.execute("""
        INSERT OR IGNORE INTO items
        (
            id,
            type,
            rarity,
            owner_id
        )
        VALUES
        (
            :id, 
            :type,
            :rarity, 
            :owner_id
        );
        """, item.db_dict)

    async def update(self, item: Item) -> None:
        await self._cursor.execute("""
        UPDATE items 
        SET 
            type=:type,
            rarity=:rarity,
            owner_id=:owner_id
        WHERE id=:id;
        """, item.db_dict)

    async def delete(self, item: Item) -> None:
        await self._cursor.execute("""
        DELETE FROM items
        WHERE id=:id;
        """, item.db_dict)
