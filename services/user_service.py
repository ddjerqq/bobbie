import aiosqlite
from models.user import User
from repositories.user_repository import UserRepository


class UserService:
    """
    The user service for the database User models
    User Repository is injected inside it and has:
    get
    add
    update
    delete
    """
    def __init__(self, connection: aiosqlite.Connection, cursor: aiosqlite.Cursor):
        self._connection = connection
        self._cursor = cursor

        self._user_repository = UserRepository(self._connection, self._cursor)

    async def get(self, id: int) -> User:
        user = await self._user_repository.get(id)
        return user

    async def add(self, id: int, username: str) -> None:
        user = User.create(id, username)
        await self._user_repository.add(user)

    async def update(self, user: User) -> None:
        await self._user_repository.update(user)

    async def delete(self, user: User) -> None:
        await self._user_repository.delete(user)
