from __future__ import annotations
from dataclasses import dataclass


@dataclass
class User(object):
    snowflake: int
    username: str
    experience: int
    wallet: int
    bank: int


    @property
    def id(self):
        return self.snowflake


    @classmethod
    def new(cls, snowflake: int, username: str) -> User:
        """
        create users with this
        :param snowflake: id of the user
        :param username:  username of the user
        :return: User object
        """
        return cls(snowflake, username, 0, 0, 0)


    @property
    def to_database(self) -> tuple:
        """
        (snowflake, username, experience, bank, wallet)
        """
        return self.snowflake, self.username, int(self.experience), int(self.bank), int(self.wallet)


    @classmethod
    def from_database(cls, data: tuple) -> User:
        """
        use this to compile database tuple into a user
        :param data: tuple(id, username, joindate, experience, wallet, bank)
        :return: User
        """
        return cls(int(data[0]), data[1], int(data[2]), int(data[3]), int(data[4]))


    def __eq__(self, other: User):
        return self.id == other.id

    def __str__(self):
        return f"({self.snowflake}) {self.username}"

