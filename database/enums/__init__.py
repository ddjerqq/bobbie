import disnake.ext.commands

from .item_config import *
from .item_random_weights import *
from .pet_config import *
from .level import *

__all__ = [
    "ItemType",
    "ItemEmoji",
    "ItemName",
    "ItemPrice",
    "ItemThumbnail",
    "Buyable",
    "PetType",
    "PetEmoji",
    "PetName",
    "PetPrice",
    "PetThumbnail",
    "LevelRanges",
    "LevelName",
    "HuntableRandomWeight",
    "DigableRandomWeight",
    "FishableRandomWeight",
    "TOOL_BUY_PRICES",
    "ITEM_SELL_PRICES",
    "PET_BUY_PRICES",
]

TOOL_BUY_PRICES = disnake.ext.commands.option_enum({
    f"{ItemName[item.name].value} {ItemPrice[item.name].value} ₾": item.value for item in Buyable
})

ITEM_SELL_PRICES = disnake.ext.commands.option_enum({
    f"{item.value} {ItemPrice[item.name].value} ₾": item.name for item in ItemName
})

PET_BUY_PRICES = disnake.ext.commands.option_enum({
    f"{PetName[pet.name].value} {PetPrice[pet.name].value} ₾": pet.value for pet in PetType
})
