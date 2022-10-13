from itertools import groupby
import aiosqlite
from database.models.user import User
from database.repositories.item_repository import ItemRepository
from database.repositories.marriage_repository import MarriageRepository
from database.repositories.pet_repository import PetRepository
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
    def __init__(self, connection: aiosqlite.Connection, cursor: aiosqlite.Cursor):
        self._connection = connection
        self._cursor = cursor
        self._user_repository = UserRepository(self._connection, self._cursor)
        self._item_repository = ItemRepository(self._connection, self._cursor)
        self._pet_repository  = PetRepository(self._connection, self._cursor)

    async def get_all(self) -> list[User | None]:
        users = await self._user_repository.get_all()
        items = await self._item_repository.get_all()
        pets  = await self._pet_repository.get_all()
        
        item_owners = {user.id: [] for user in users}
        for item in items:
            item_owners[item.owner_id].append(item)
            
        pet_owners  = {user.id: [] for user in users}
        for pet in pets:
            pet_owners[pet.owner_id].append(pet)

        for user in users:
            user.items = item_owners.get(user.id, [])
            user.pets  = pet_owners.get(user.id, [])

        return users

    async def get(self, id: int) -> User | None:
        user  = await self._user_repository.get(id)
        items = await self._item_repository.get_all()
        pets  = await self._pet_repository.get_all()

        if user is not None:
            user.items = list(filter(lambda item: item.owner_id == user.id, items))
            user.pets  = list(filter(lambda entity: entity.owner_id == user.id, pets))

        return user

    async def add(self, entity: User) -> None:
        await self._user_repository.add(entity)
        for item in entity.items:
            await self._item_repository.add(item)

        for pet in entity.pets:
            await self._pet_repository.add(pet)

        await self._user_repository.save_changes()
        await self._item_repository.save_changes()
        await self._pet_repository.save_changes()

    async def update(self, entity: User) -> None:
        await self._user_repository.update(entity)
        # region UPDATE ITEMS
        db_items = await self._item_repository.get_all()

        for item in entity.items:
            if item in db_items:
                await self._item_repository.update(item)
            else:
                await self._item_repository.add(item)

        for item in filter(lambda i: i.owner_id == entity.id, db_items):
            if item not in entity.items:
                await self._item_repository.delete(item)
        # endregion
        # region UPDATE PETS
        db_pets = await self._pet_repository.get_all()

        for pet in entity.pets:
            if pet in db_pets:
                await self._pet_repository.update(pet)
            else:
                await self._pet_repository.add(pet)

        for pet in filter(lambda p: p.owner_id == entity.id, db_pets):
            if pet not in entity.pets:
                await self._pet_repository.delete(pet)
        # endregion
        await self._user_repository.save_changes()
        await self._item_repository.save_changes()
        await self._pet_repository.save_changes()

    async def delete(self, entity: User) -> None:
        await self._user_repository.delete(entity)

        for item in entity.items:
            await self._item_repository.delete(item)

        for pet in entity.pets:
            await self._pet_repository.delete(pet)

        await self._user_repository.save_changes()
        await self._item_repository.save_changes()
