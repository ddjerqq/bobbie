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


async def give_exp(id: int, xp_amount: int) -> None:
    await database.users.add_experience(id, xp_amount)


async def get_user_balance(id: int) -> tuple[int, int]:
    """
    get the bank and wallet of a user
    """
    bank, wallet = await database.users.get_user_balance(id)
    return bank, wallet


async def deposit(user_id: int, amount: int) -> bool:
    """
    deposit from wallet to bank
    :return: returns boolean true if transaction is successful, else false
    """
    bank, wallet = await database.users.get_user_balance(user_id)

    if amount > wallet:
        return False

    await database.users.wallet(user_id, -amount)
    await database.users.bank(user_id, amount)
    return True


async def withdraw(user_id: int, amount: int) -> bool:
    """
    withdraw from bank to wallet
    :return: returns boolean true if transaction is successful, else false
    """
    bank, wallet = await database.users.get_user_balance(user_id)
    if amount > bank:
        return False
    await database.users.bank(user_id, -amount)
    await database.users.wallet(user_id, amount)
    return True


async def give(sender: int, receiver: int, amount: int) -> bool:
    _, sender_wallet = get_user_balance(sender)

    if amount > sender_wallet:
        return False

    await database.users.wallet(sender, -amount)
    await database.users.wallet(receiver, amount)

    log(f"{sender} -> {receiver} : {amount}")


async def work(user_id: int) -> None:
    """
    work command, gives users 10 money
    """
    await database.users.wallet(user_id, 10)

