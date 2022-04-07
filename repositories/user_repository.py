import aiosqlite
from models.user import User


class UserRepository:
    def __init__(self, connection: aiosqlite.Connection, cursor: aiosqlite.Cursor):
        self._connection = connection
        self._cursor     = cursor
        self._queue      = 0

    async def _commit(self):
        if not self._queue % 3:
            await self._connection.commit()
        self._queue += 1

    async def get(self, id: int) -> User | None:
        await self._cursor.execute("""
        SELECT * FROM users
        WHERE snowflake=?
        """, (id,))

        data = await self._cursor.fetchone()

        if data is not None:
            user = User.from_database(tuple(data))
            return user

        return None

    async def add(self, user: User) -> None:
        await self._cursor.execute("""
        INSERT INTO users
        VALUES(?, ?, ?, ?, ?)
        """, user.to_database)

        await self._commit()

    async def update(self, user: User) -> None:
        old = await self.get(user.id)

        if user.username != old.username:
            await self._cursor.execute("""
            UPDATE users 
            SET username=?
            WHERE snowflake=?
            """, (user.username, user.id))

        if user.experience != old.experience:
            await self._cursor.execute("""
            UPDATE users 
            SET experience=?
            WHERE snowflake=?
            """, (user.experience, user.id))

        if user.bank != old.bank:
            await self._cursor.execute("""
            UPDATE users 
            SET bank=?
            WHERE snowflake=?
            """, (user.bank, user.id))

        if user.wallet != old.wallet:
            await self._cursor.execute("""
            UPDATE users 
            SET wallet=?
            WHERE snowflake=?
            """, (user.wallet, user.id))

        await self._commit()

    async def delete(self, user: User) -> None:
        await self._cursor.execute("""
        DELETE FROM users
        WHERE snowflake=?
        """, user.id)

        await self._commit()
