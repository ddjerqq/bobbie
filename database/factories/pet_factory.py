from database.enums import *
from database.id import Id
from database.models.pet import Pet
import random

from database.rarity import Rarity


class PetFactory:
    @classmethod
    def new(cls, item_type: PetType) -> Pet:
        """
        create a new pet with a random id, rarity, 0 level and no owner id
        """
        id = Id.new()
        rarity = Rarity.new()
        return Pet(id, item_type, rarity, 0, None)

    @classmethod
    def from_db_row(cls, data: tuple[int, str, float, int, int]) -> Pet:
        id        = data[0]
        item_type = PetType[data[1].upper()]
        rarity    = Rarity(data[2])
        level     = data[3]
        owner_id  = data[4]
        return Pet(id, item_type, rarity, level, owner_id)
