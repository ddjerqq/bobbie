from __future__ import annotations
from datetime import datetime
from typing import overload
from typing import Any


class User(object):
    def __init__(self,
                 snowflake: int,
                 username: str,
                 join_date: datetime,
                 experience: int = 0) -> None:
        """
        `DO NOT USE THIS TO CREATE USERS!` \n
        use User.create() instead.
        """
        self.snowflake  = snowflake
        self.username   = username
        self.join_date  = join_date
        self.experience = experience

    @property
    def id(self):
        return self.snowflake

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

    @property
    def to_database(self) -> tuple:
        """
        decompile a user to a tuple for storing in the database
        :return: tuple (id, username, joindate, experience)
        """
        return self.snowflake, self.username, self.join_date, self.experience


    @classmethod
    def from_database(cls, data: tuple) -> User:
        """
        use this to compile database tuple into a user
        :param data: tuple(id, username, joindate)
        :return: User
        """
        return cls(data[0], data[1], data[2], data[3])

    def __str__(self):
        return f"({self.snowflake}) {self.username}"

