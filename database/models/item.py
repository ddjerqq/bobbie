from __future__ import annotations

import random
import sqlite3
from datetime import datetime

from database.id import Id
from database.config import *


class Item:
    """
    Item class, with UNIQUE ID generation, and rarity float generation.
    -------------------------------------------------------------------
    rarities:
        (0.00; 0.07] => Factory New
        (0.07; 0.15] => Minimal Wear
        (0.15; 0.38] => Field-Tested
        (0.38; 0.45] => Well-Worn
        (0.45; 1.00] => Battle-Scarred
    """

    def __init__(self, id: int, type: ItemType, rarity: float, owner_id: int | None):
        self.__broken = None  # type: bool | None
        self.__id = id
        self.type = type
        self.__rarity = rarity
        self.owner_id = owner_id

    # TODO move this to factory
    @classmethod
    def new(cls, type: str) -> Item:
        id = Id.new()
        rarity = random.random() ** 2
        return cls(id, type, rarity, None)

    @property
    def id(self) -> int:
        return self.__id

    @property
    def price(self) -> int:
        p = ItemPrice[self.type.name].value
        p += 1 / self.rarity
        return round(p)

    @property
    def buyable(self):
        """
        :return: bool if the item is in {"fishing_rod", "hunting_rifle", "shovel"}
        """
        try:
            Buyable[self.type.name]
        except KeyError:
            return False
        else:
            return True

    @property
    def emoji(self) -> str | None:
        """get the emoji of this item type, if it is missing, then this will return an empty string"""
        try:
            emoji = ItemEmoji[self.type.name].value
        except KeyError:
            emoji = ""
        return emoji

    @property
    def thumbnail(self) -> str | None:
        """get the item's thumbnail. if its missing, returns None"""
        try:
            thumbnail = ItemThumbnail[self.type.name].value
        except KeyError:
            thumbnail = None
        return thumbnail

    @property
    def name(self) -> str:
        """get the item's name"""
        return ItemName[self.type.name].value

    @property
    def rarity_string(self) -> str:
        if   0.0 <= self.__rarity <= 0.07:
            return "სულ ახალი"
        elif 0.07 < self.__rarity <= 0.15:
            return "მინიმალურად გამოყენებული"
        elif 0.15 < self.__rarity <= 0.38:
            return "ოდნავ გამოყენებული"
        elif 0.38 < self.__rarity <= 0.45:
            return "კარგად ნახმარი"
        elif 0.45 < self.__rarity <= 1.00:
            return "დაგლეჯილი"
        else:
            raise ValueError(f"Invalid rarity: {self.__rarity}")

    @property
    def rarity(self) -> float:
        return self.__rarity

    @property
    def created_at(self) -> datetime:
        """
        get the creation datetime of Item.
        .strftime("%Y-%m-%d %H:%M:%S")
        :return datetime:
        """
        return Id.created_at(self.__id)

    @property
    def will_break(self) -> bool:
        """try break the item, return True if the item broke"""
        if not self.__broken:
            self.__broken = random.random() < self.__rarity ** 2.5
        return self.__broken

    def __hash__(self):
        return hash(self.db)

    def __eq__(self, other):
        return isinstance(other, Item) and self.__id == other.__id

    def __str__(self):
        return f"{self.type.name} {self.rarity_string} owner: {self.owner_id}"

    def __repr__(self):
        return f"<Item id={self.id} type={self.type} owner={self.owner_id} rarity={self.__rarity}>"

    # TODO make this return a dict
    @property
    def db(self) -> tuple:
        return self.__id, self.type, self.__rarity, self.owner_id

    # TODO move this to factory
    @classmethod
    def from_db_row(cls, data: sqlite3.Row) -> Item:
        return cls(**dict(data))

    def use(self) -> Item:
        """
        generate a random item from the given type of the tool.
        :return: an item of the given type
        """
        match self.type:
            case ItemType.FISHING_ROD:
                group = FishableRandomWeight
            case ItemType.HUNTING_RIFLE:
                group = HuntableRandomWeight
            case ItemType.SHOVEL:
                group = DigableRandomWeight
            case _:
                raise ValueError(f"item type '{self.type}' is not a valid tool, must be one of {[*Buyable]}")

        random_type = random.choice(list(iter(group)))

        return self.new(random_type)

    # TODO factory pattern
    @classmethod
    def random_item(cls) -> Item:
        """generate a random item"""
        random_type = random.choice(list(iter(ItemType)))
        return cls.new(random_type)
