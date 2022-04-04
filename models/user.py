from __future__ import annotations
from datetime import datetime
from typing import overload
from typing import Any


class User(object):
    def __init__(self,
                 snowflake: int,
                 username: str,
                 join_date: datetime,
                 experience: int = 0,
                 wallet: int = 0,
                 bank: int = 0) -> None:
        """
        `DO NOT USE THIS TO CREATE NEW USERS!` \n
        use User.create() instead.
        """
        self.snowflake  = snowflake
        self.username   = username
        self.join_date  = join_date
        self.experience = experience
        self.wallet     = wallet
        self.bank       = bank

    @property
    def id(self):
        return self.snowflake

    @property
    def to_database(self) -> tuple:
        return self.snowflake, self.username, self.join_date, self.experience, self.bank, self.wallet


    @classmethod
    def create(cls, snowflake: int, username: str, join_date: datetime) -> User:
        """
        create users with this
        :param snowflake: id of the user
        :param username:  username of the user
        :param join_date: datetime object of the users join date
        :return: User object
        """
        return cls(snowflake, username, join_date)


    @classmethod
    def from_database(cls, data: tuple) -> User:
        """
        use this to compile database tuple into a user
        :param data: tuple(id, username, joindate)
        :return: User
        """
        print(data)
        return cls(data[0], data[1], data[2], data[3], data[4], data[5])


    def __str__(self):
        return f"({self.snowflake}) {self.username}"

