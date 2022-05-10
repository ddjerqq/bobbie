import aiosqlite
from database.models.user import User
from database.repositories.item_repository import ItemRepository
from database.repositories.user_repository import UserRepository


class UserService:
    """
    The user service for the database User models
    User Repository is injected inside it and has:
    get
    add return user obj
    update
    delete
    """
    # TODO V3 feature, allitems cached, cuz idk why
    # why not + fun to make
    def __init__(self, connection: aiosqlite.Connection, cursor: aiosqlite.Cursor):
        self._connection = connection
        self._cursor = cursor
        self._user_repository = UserRepository(self._connection, self._cursor)
        self._item_repository = ItemRepository(self._connection, self._cursor)

    async def get_all(self) -> list[User | None]:
        items = await self._item_repository.get_all()
        users = await self._user_repository.get_all()

        for user in users:
            user.items = list(filter(lambda item: item.owner_id == user.id, items))

        return users

    async def get(self, id: int) -> User | None:
        items = await self._item_repository.get_all()
        user  = await self._user_repository.get(id)

        if user is not None:
            user.items = list(filter(lambda item: item.owner_id == user.id, items))

        return user

    async def add(self, user: User) -> None:
        await self._user_repository.add(user)
        for item in user.items:
            await self._item_repository.add(item)

        await self._user_repository.save_changes()
        await self._item_repository.save_changes()

    async def update(self, user: User) -> None:
        await self._user_repository.update(user)

        old_items = await self._item_repository.get_all()
        old_items = list(filter(lambda i: i.owner_id == user.id, old_items))

        deleted_items = list(filter(lambda i: i not in user.items, old_items))
        new_items = set(user.items) - set(old_items)
        update_me = set(old_items) - set(new_items) - set(deleted_items)

        for item in deleted_items:
            await self._item_repository.delete(item)

        for item in new_items:
            await self._item_repository.add(item)

        for item in update_me:
            await self._item_repository.update(item)

        await self._user_repository.save_changes()
        await self._item_repository.save_changes()

    async def delete(self, user: User) -> None:
        await self._user_repository.delete(user)
        for item in user.items:
            await self._item_repository.delete(item)

        await self._user_repository.save_changes()
        await self._item_repository.save_changes()
