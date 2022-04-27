import aiosqlite
from models.item import Item
from repositories.item_repository import ItemRepository


class ItemService:
    """
    ItemRepository is injected inside it and has:
    get
    add
    update
    delete
    """
    def __init__(self, connection: aiosqlite.Connection, cursor: aiosqlite.Cursor):
        self._connection = connection
        self._cursor = cursor
        self._item_repository = ItemRepository(self._connection, self._cursor)

    async def get_all_by_owner_id(self, owner_id: int) -> list[Item | None]:
        items = await self._item_repository.get_all()
        return list(filter(lambda item: item.owner_id == owner_id, items))

    async def del_all_by_owner_id(self, owner_id: int) -> None:
        items = await self.get_all_by_owner_id(owner_id)
        for item in items:
            await self._item_repository.delete(item)
        await self._item_repository.save_changes()

    async def get_all(self) -> list[Item | None]:
        items = await self._item_repository.get_all()
        return items

    async def get(self, id: int) -> Item:
        item = await self._item_repository.get(id)
        return item

    async def add(self, item: Item) -> None:
        await self._item_repository.add(item)
        await self._item_repository.save_changes()

    async def update(self, item: Item) -> None:
        await self._item_repository.update(item)
        await self._item_repository.save_changes()

    async def delete(self, item: Item) -> None:
        await self._item_repository.delete(item)
        await self._item_repository.save_changes()
