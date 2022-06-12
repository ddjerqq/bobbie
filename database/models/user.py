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

    @property
    def db_dict(self) -> dict:
        """
        {
            "id": self.__id,
            "username": self.username,
            "experience": self.experience,
            "wallet": self.wallet,
            "bank": self.bank
        }
        """
        return {"id": self.__id, "username": self.username,
                "experience": self.experience, "bank": self.bank,
                "wallet": self.wallet}

    def __hash__(self):
        return hash(self.__id)

    def __eq__(self, other: User):
        return isinstance(other, User) and self.__id == other.__id

    def __repr__(self):
        return f"<User id={self.__id} username={self.username}>"

    def __str__(self):
        return f"({self.__id}) {self.username}"

