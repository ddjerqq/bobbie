from __future__ import annotations

from datetime import datetime

from database.id import Id
from database.enums import *
from database.rarity import *


class Pet:
    """
    the pet class with unique id generation and rarity
    """
    def __init__(self,
                 id: int,
                 type: PetType,
                 rarity: Rarity,
                 level: int,
                 owner_id: int | None,
                 ) -> None:
        self.__id = id
        self.type = type
        self.rarity = rarity
        self.level = level
        self.owner_id = owner_id

    @property
    def id(self):
        return self.__id

    @property
    def price(self) -> int:
        p  = PetPrice[self.type.name].value
        p += 1 / self.rarity.value
        return round(p)

    @property
    def level_name(self) -> str:
        level_type = next((level for level in LevelRanges if self.level in level.value), LevelRanges.MAX)
        level_name = LevelName[level_type.name].value
        return level_name

    @property
    def emoji(self) -> str:
        try:
            emoji = PetEmoji[self.type.name].value
        except KeyError:
            emoji = ""
        return emoji

    @property
    def thumbnail(self) -> str | None:
        try:
            thumbnail = PetThumbnail[self.type.name].value
        except KeyError:
            thumbnail = None
        return thumbnail

    @property
    def name(self) -> str:
        """get the item's name ქართულად"""
        return PetName[self.type.name].value

    @property
    def created_at(self) -> datetime:
        """
        get the creation datetime of Item.
        use user.created_at.strftime("%Y-%m-%d %H:%M:%S")
        """
        return Id.created_at(self.__id)

    @property
    def db_dict(self) -> dict:
        """
        id, type, rarity, level, owner_id
        """
        return {
            "id": self.__id,
            "type": self.type.name.lower(),
            "rarity": self.rarity.value,
            "level": self.level,
            "owner_id": self.owner_id,
        }

    def __hash__(self):
        return hash(self.__id)

    def __eq__(self, other):
        return isinstance(other, Pet) and self.__id == other.__id

    def __str__(self):
        return f"{self.type.name} {self.rarity.name} owner: {self.owner_id}"

    def __repr__(self):
        return f"<Pet id={self.id} type={self.type.name} owner={self.owner_id} level={self.level} rarity={self.rarity!r}>"
