from __future__ import annotations

import random
import sqlite3
from datetime import datetime

from database.id import Id
from database.config import *
from database.rarity import Rarity


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

    def __init__(self, id: int, type: ItemType, rarity: Rarity, owner_id: int | None):
        self.__id = id
        self.type = type
        self.rarity = rarity
        self.owner_id = owner_id

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
        check if the item is
        {"fishing_rod", "hunting_rifle", "shovel", "knife"}
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
    def created_at(self) -> datetime:
        """
        get the creation datetime of Item.
        .strftime("%Y-%m-%d %H:%M:%S")
        :return datetime:
        """
        return Id.created_at(self.__id)

    def __hash__(self):
        return hash(self.db)

    def __eq__(self, other):
        return isinstance(other, Item) and self.__id == other.__id

    def __str__(self):
        return f"{self.type.name} {self.rarity.name} owner: {self.owner_id}"

    def __repr__(self):
        return f"<Item id={self.id} type={self.type.name} owner={self.owner_id} rarity={self.rarity!r}>"

    # TODO make this return a dict
    @property
    def db(self) -> tuple:
        return self.__id, self.type, self.__rarity, self.owner_id

    # TODO factory pattern
    @classmethod
    def random_item(cls) -> Item:
        """generate a random item"""
        random_type = random.choice(list(iter(ItemType)))
        return cls.new(random_type)
