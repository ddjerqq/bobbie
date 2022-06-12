import sqlite3

from database.config import *
from database.id import Id
from database.models.item import Item
import random

from database.rarity import Rarity


class ItemFactory:
    @classmethod
    def new(cls, item_type: ItemType) -> Item:
        """
        create a new item with a random id, rarity and no owner id
        """
        id = Id.new()
        rarity = Rarity.new()
        return Item(id, item_type, rarity, None)

    @classmethod
    def from_db_row(cls, data: sqlite3.Row) -> Item:
        data = dict(data)
        id        = data.pop("id")
        item_type = ItemType[data.pop("item_type").upper()]
        rarity    = Rarity(data.pop("rarity"))
        owner_id  = data.pop("owner_id")
        return Item(id, item_type, rarity, owner_id)

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
