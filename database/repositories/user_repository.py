import aiosqlite

from database.factories.user_factory import UserFactory
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
        await self._cursor.execute("""
        SELECT * FROM users;
        """)
        rows = await self._cursor.fetchall()
        return [UserFactory.from_db_row(row) for row in rows]

    async def get(self, id: int) -> User | None:
        await self._cursor.execute("""
        SELECT * FROM users
        WHERE snowflake=?;
        """, (id,))
        data = await self._cursor.fetchone()
        if data is not None:
            data = UserFactory.from_db_row(data)
        return data

    async def add(self, user: User) -> None:
        await self._cursor.execute("""
        INSERT OR IGNORE INTO users
        (
            snowflake,
            username,
            experience,
            bank,
            wallet
        )
        VALUES
        (
            :id, 
            :username, 
            :experience,
            :bank, 
            :wallet
        );
        """, user.db_dict)

    async def update(self, user: User) -> None:
        await self._cursor.execute("""
        UPDATE users 
        SET 
            username=:username,
            experience=:experience,
            bank=:bank,
            wallet=:wallet
        WHERE snowflake=:id;
        """, user.db_dict)

    async def delete(self, user: User) -> None:
        await self._cursor.execute("""
        DELETE FROM users
        WHERE snowflake=:id;
        """, user.db_dict)
