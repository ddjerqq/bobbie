import aiosqlite
from database.models.marriage import Marriage
from database.repositories.marriage_repository import MarriageRepository


class MarriageService:
    """
    The marriage service for managing marriages and the roles.
    """

    def __init__(self, connection: aiosqlite.Connection, cursor: aiosqlite.Cursor):
        self._connection      = connection
        self._cursor          = cursor
        self._marriages_repository = MarriageRepository(self._connection, self._cursor)

    async def get_all(self) -> list[Marriage | None]:
        return await self._marriages_repository.get_all()

    async def get(self, id: int) -> Marriage | None:
        return await self._marriages_repository.get(id)

    async def add(self, entity: Marriage) -> None:
        await self._marriages_repository.add(entity)

    async def update(self, entity: Marriage) -> None:
        await self._marriages_repository.update(entity)

    async def delete(self, entity: Marriage) -> None:
        await self._marriages_repository.delete(entity)
