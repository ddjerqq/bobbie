from database.enums import *
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
    def from_db_row(cls, data: tuple[int, str, float, int]) -> Item:
        id        = data[0]
        item_type = ItemType[data[1].upper()]
        rarity    = Rarity(data[2])
        owner_id  = data[3]
        return Item(id, item_type, rarity, owner_id)

    @classmethod
    def use(cls, item: Item) -> tuple[Item | None, bool | None]:
        """
        return the result of the usage of the item.
        (item, broken)
        if the item is knife, this will return only only broken
        """
        broken = random.random() < item.rarity.value ** 2.5

        match item.type:
            case ItemType.FISHING_ROD:
                group = FishableRandomWeight
            case ItemType.HUNTING_RIFLE:
                group = HuntableRandomWeight
            case ItemType.SHOVEL:
                group = DigableRandomWeight
            case ItemType.KNIFE:
                return None, broken
            case _:
                return None, None

        random_type = random.choice(list(iter(group)))

        return cls.new(random_type), broken
