import sqlite3

from database.config import *
from database.id import Id
from database.models.item import Item
import random


class ItemFactory:
    @classmethod
    def new(cls, item_type: ItemType) -> Item:
        id = Id.new()
        rarity = random.random() ** 2
        return Item(id, item_type, rarity, None)

    @classmethod
    def from_db_row(cls, data: sqlite3.Row) -> Item:
        return Item(**dict(data))

    @classmethod
    def use(cls, item: Item) -> Item | None:
        """
        simulate using the item, optionally returns a new item,
        the booty of the item use
        """
        if random.random() < item.rarity.value ** 2.5:
            return None

        match item.type:
            case ItemType.FISHING_ROD:
                group = FishableRandomWeight
            case ItemType.HUNTING_RIFLE:
                group = HuntableRandomWeight
            case ItemType.SHOVEL:
                group = DigableRandomWeight
            case _:
                return None

        random_type = random.choice(list(iter(group)))

        return cls.new(random_type)



for _ in range(10):
    item = ItemFactory.use(ItemFactory.new(ItemType.FISHING_ROD))
    print(item)
