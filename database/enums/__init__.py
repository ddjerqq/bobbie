import disnake.ext.commands

from .item_config import *
from .item_random_weights import *
from .pet_config import *

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
    "HuntableRandomWeight",
    "DigableRandomWeight",
    "FishableRandomWeight",
    "TOOL_BUY_PRICES",
    "ITEM_SELL_PRICES",
]

TOOL_BUY_PRICES = disnake.ext.commands.option_enum({
    f"{ItemName[item.name].value[0]} {ItemPrice[item.name].value} ₾": item.value for item in Buyable
})

ITEM_SELL_PRICES = disnake.ext.commands.option_enum({
    f"{item.value[0]} {ItemPrice[item.name].value} ₾": item.name for item in ItemName
})
