import disnake.ext.commands

from . emoji import *
from . names import *
from . prices import *
from . random_chance_weights import *
from . thumbnails import *
from . tools import *
from . item_types import *

__all__ = ["ItemEmoji", "ItemName", "ItemPrice",
           "HuntableRandomWeight", "DigableRandomWeight",
           "FishableRandomWeight", "ItemThumbnail",
           "Buyable", "ItemType",
           "TOOL_BUY_PRICES", "ITEM_SELL_PRICES"]

TOOL_BUY_PRICES = disnake.ext.commands.option_enum({
    f"{ItemName[item.name].value[0]} {ItemPrice[item.name].value} ₾": item.name for item in Buyable
})

ITEM_SELL_PRICES = disnake.ext.commands.option_enum({
    f"{item.value[0]} {ItemPrice[item.name].value} ₾": item.name for item in ItemName
})
