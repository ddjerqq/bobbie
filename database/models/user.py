from __future__ import annotations

import sqlite3

from database.models.item import Item


class User(object):
    def __init__(self, id: int, username: str, experience: int, wallet: int, bank: int) -> None:
        self.__id = id
        self.username = username
        self.experience = experience
        self.wallet = wallet
        self.bank = bank

        self.items = []  # type: list[Item]

    @property
    def id(self):
        return self.__id

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
    def db(self) -> tuple:
        """
        (snowflake, username, experience, bank, wallet)
        """
        return self.__id, self.username, int(self.experience), int(self.bank), int(self.wallet)

    @classmethod
    def from_db(cls, data: tuple | sqlite3.Row) -> User:
        return cls(*data)

    def __hash__(self):
        return hash(self.db)

    def __eq__(self, other: User):
        return self.id == other.id

    def __repr__(self):
        return f"<{self.__class__} id={self.__id} username={self.username} at {hex(id(self))}>"

    def __str__(self):
        return f"({self.__id}) {self.username}"

