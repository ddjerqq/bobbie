import aiosqlite
from database.models.item import Item


class ItemRepository:
    """
    it's your responsibility to commit the changes to the database
    """
    def __init__(self, connection: aiosqlite.Connection, cursor: aiosqlite.Cursor):
        self._connection = connection
        self._cursor = cursor

    async def save_changes(self):
        await self._connection.commit()

    async def get_all(self) -> list[Item | None]:
        await self._cursor.execute("SELECT * FROM items")
        items = await self._cursor.fetchall()
        return [Item.from_db(tuple(item)) for item in items]

    async def get(self, id: int) -> Item | None:
        await self._cursor.execute("""
        SELECT * FROM items 
        WHERE id=?""", (id,))
        data = await self._cursor.fetchone()
        return data if data is None else Item.from_db(data)

    async def add(self, item: Item) -> None:
        exists = await self.get(item.id)
        if isinstance(exists, Item):
            return

        await self._cursor.execute("""
        INSERT INTO items
        VALUES(?, ?, ?, ?)
        """, item.db)

    async def update(self, item: Item) -> None:
        await self._cursor.execute("""
        UPDATE items 
        SET owner_id=?
        WHERE id=?
        """, (item.owner_id, item.id))

    async def delete(self, item: Item) -> None:
        await self._cursor.execute("""
        DELETE FROM items
        WHERE id=?
        """, (item.id,))
