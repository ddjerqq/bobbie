from __future__ import annotations

from database.models.item import Item
from database.models.pet import Pet


class User(object):
    def __init__(self, id: int, username: str, experience: int, wallet: int, bank: int, marriage_id: int | None) -> None:
        self.__id = id
        self.username = username
        self.experience = experience
        self.wallet = wallet
        self.bank = bank

        self.items = []  # type: list[Item]
        self.pets  = []  # type: list[Pet]

        self.marriage_id = marriage_id

    @property
    def id(self):
        return self.__id

    @property
    def db_dict(self) -> dict:
        """
        {
            id
            username
            experience
            wallet
            bank
            marriage_id
        }
        """
        return {
            "id": self.__id,
            "username": self.username,
            "experience": self.experience,
            "wallet": self.wallet,
            "bank": self.bank,
            "marriage_id": self.marriage_id,
        }

    def __hash__(self):
        return hash(self.__id)

    def __eq__(self, other: User):
        return isinstance(other, User) and self.__id == other.__id

    def __repr__(self):
        return f"<Db.User id={self.__id} username={self.username}>"

    def __str__(self):
        return f"({self.__id}) {self.username}"
