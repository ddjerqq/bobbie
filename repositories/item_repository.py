import aiosqlite
from models.item import Item


class ItemRepository:
    def __init__(self, connection: aiosqlite.Connection, cursor: aiosqlite.Cursor):
        self._connection = connection
        self._cursor = cursor

    async def save_changes(self):
        await self._connection.commit()

    async def get_all_by_owner_id(self, owner_id) -> list[Item]:
        await self._cursor.execute("""
        SELECT * FROM items
        WHERE owner_id=?
        """, (owner_id,))

        items = await self._cursor.fetchall()

        return [Item.from_database(tuple(item)) for item in items]

    async def get(self, id: int) -> Item | None:
        await self._cursor.execute("SELECT * FROM items WHERE id=?", (id,))
        item = await self._cursor.fetchone()

        if item is None:
            return None

        return Item.from_database(tuple(item))

    async def add(self, item: Item) -> None:
        exists = await self.get(item.id)
        if isinstance(exists, Item):
            return

        await self._cursor.execute("""
        INSERT INTO items
        VALUES(?, ?, ?, ?)
        """, item.to_database)

    async def update(self, item: Item) -> None:
        old = await self.get(item.id)

        if old is None:
            await self.add(item)
            return

        if item.owner_id != old.owner_id:
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
