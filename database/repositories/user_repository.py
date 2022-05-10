import aiosqlite
from database.models.user import User


class UserRepository:
    """
    it's your responsibility to commit the changes to the database
    """
    def __init__(self, connection: aiosqlite.Connection, cursor: aiosqlite.Cursor):
        self._connection = connection
        self._cursor     = cursor

    async def save_changes(self):
        await self._connection.commit()

    async def get_all(self) -> list[User | None]:
        await self._cursor.execute("SELECT * FROM users")
        users = await self._cursor.fetchall()
        return [User.from_db(tuple(user)) for user in users]

    async def get(self, id: int) -> User | None:
        await self._cursor.execute("""
        SELECT * FROM users
        WHERE snowflake=?
        """, (id,))

        data = await self._cursor.fetchone()

        if data is not None:
            user = User.from_db(data)
            return user

        return None

    async def add(self, user: User) -> None:
        await self._cursor.execute("""
        INSERT OR IGNORE INTO users
        VALUES(?, ?, ?, ?, ?)
        """, user.db)

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

    async def delete(self, user: User) -> None:
        await self._cursor.execute("""
        DELETE FROM users
        WHERE snowflake=?
        """, user.id)
