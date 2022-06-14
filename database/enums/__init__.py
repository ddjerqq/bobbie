import disnake.ext.commands

from .item_emoji import *
from .item_name import *
from .item_price import *
from .fishable_weight import *
from .huntable_weight import *
from .digable_weight import *
from .buyable import *
from .item_thumbnail import *
from .item_type import *

__all__ = ["ItemEmoji", "ItemName", "ItemPrice",
           "HuntableRandomWeight", "DigableRandomWeight",
           "FishableRandomWeight", "ItemThumbnail",
           "Buyable", "ItemType",
           "TOOL_BUY_PRICES", "ITEM_SELL_PRICES"]

TOOL_BUY_PRICES = disnake.ext.commands.option_enum({
    f"{ItemName[item.name].value[0]} {ItemPrice[item.name].value} ₾": item.value for item in Buyable
})

ITEM_SELL_PRICES = disnake.ext.commands.option_enum({
    f"{item.value[0]} {ItemPrice[item.name].value} ₾": item.name for item in ItemName
})
