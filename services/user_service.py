"""
User service, use this in the front end
"""

from utils import *

from models.database.database import database
from models.user import User


async def get_by_id(id: int) -> User | None:
    """
    use this to get a user by their id
    :param id: snowflake discord id
    :return: User object
    """
    user = await database.users.get_by_id(id)
    return user


async def add_user(id: int, username: str, joindate: datetime) -> None:
    """
    add user to the database
    :param id:
    :param username:
    :param joindate:
    :return:
    """
    user = User.create(id, username, joindate)
    log(f"added new user \n{user}")
    await database.users.add_user(user)


async def update_username(id: int, username: str):
    await database.users.update_name(id, username)


async def add_xp(id: int, xp_amount: int) -> None:
    await database.users.add_experience(id, xp_amount)




