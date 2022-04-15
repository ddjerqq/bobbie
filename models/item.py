from __future__ import annotations

import time
import random
from dataclasses import dataclass
from disnake.ext.commands import option_enum


# 2004/02/16 10 am
_GIO_EPOCH = 107691120000

FISHES = {
    "common_fish": 5,
    "rare_fish": 10,
    "tropical_fish_": 20,
    "shark": 40,
    "golden_fish": 50,
}

ANIMALS = {
    "pig": 5,
    "deer": 10,
    "bear": 20,
    "wolf": 30,
    "tiger": 40,
    "lion": 50,
    "elephant": 60,
}

DUG_ITEMS = {
    "copper_coin": 1,
    "emerald"    : 10,
    "ruby"       : 20,
    "sapphire"   : 30,
    "amethyst"   : 40,
    "diamond"    : 50,
}

ITEMS_AND_PRICES = {
    "fishing_rod": 15,
    "hunting_rifle": 20,
    "shovel": 15,
}

EMOJIS = {
    "fishing_rod": "<:fishingrod:963895429248999454>",
    "hunting_rifle": "<:huntingrifle:963895472286756945>",
    "shovel": "<:shovel:964200167001686016>",
    "common_fish" : "<:common_fish:964635049859371049>",
    "rare_fish" : "<:rare_fish:964635026534842418>",
    "tropical_fish_" : "<:tropical_fish_:964634994742005770>",
    "shark" : "<:shark_:964635075922759680>",
    "golden_fish" : "<:goldenfish:964514375027286056>",
    "pig" : "",
    "deer" : "",
    "bear" : "",
    "wolf" : "",
    "tiger" : "",
    "lion" : "",
    "elephant": "",
    "copper_coin" : "",
    "emerald" : "",
    "ruby" : "",
    "sapphire" : "",
    "amethyst" : "",
    "diamond" : ""
}

EMOJI_THUMBNAILS = {
    "fishing_rod" : "https://i.imgur.com/m7HBPHl.png",
    "hunting rifle" : "https://i.imgur.com/pjtWTSg.png",
    "shovel" : "https://i.imgur.com/Dod0FE4.png",
    "common_fish" : "",
    "rare_fish" : "",
    "tropical_fish" : "",
    "shark" : "",
    "golden_fish" : "",
    "pig" : "",
    "deer" : "",
    "bear" : "",
    "wolf" : "",
    "tiger" : "",
    "lion" : "",
    "elephant": "",
    "copper_coin" : "",
    "emerald" : "",
    "ruby" : "",
    "sapphire" : "",
    "amethyst" : "",
    "diamond" : ""
}

ITEMS_AND_PRICES.update(FISHES)
ITEMS_AND_PRICES.update(ANIMALS)
ITEMS_AND_PRICES.update(DUG_ITEMS)

BUYABLE = {"fishing_rod", "hunting_rifle", "shovel"}

TOOL_BUY_PRICES = option_enum({
    f"₾{ITEMS_AND_PRICES[i]:<3} {i}": i for i in BUYABLE
})

ITEM_ENUM = option_enum({
    k: k for k in ITEMS_AND_PRICES.keys()
})



@dataclass
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
    _id: int
    type: str
    _rarity: float
    owner_id: int | None

    @classmethod
    def new(cls, type: str) -> Item:
        """
        Create an item, with an unique id which is generated depending on the timestamp
        and _GIO_EPOCH, which is the author's birth time.
        """
        ts = int(time.time() * 100)
        id = (ts - _GIO_EPOCH) << 22
        rarity = (random.random() ** 1.5)

        return cls(id, type, rarity, None)

    @property
    def price(self) -> int:
        p = ITEMS_AND_PRICES[self.type]
        p += 1 / self._rarity
        return round(p)

    @property
    def id(self) -> int:
        return self._id

    @property
    def rarity_string(self) -> str:
        if 0.0 <= self._rarity <= 0.07:
            return "Factory New"
        elif 0.07 < self._rarity <= 0.15:
            return "Minimal Wear"
        elif 0.15 < self._rarity <= 0.38:
            return "Field-Tested"
        elif 0.38 < self._rarity <= 0.45:
            return "Well-Worn"
        elif 0.45 < self._rarity <= 1.00:
            return "Battle-Scarred"
        else:
            raise ValueError(f"Invalid rarity: {self._rarity}")

    @property
    def rarity(self) -> float:
        return self._rarity

    @property
    def creation_date(self) -> int:
        """get the creation date of Item, using _GIO_EPOCH as the base."""
        return ((self.id >> 22) + _GIO_EPOCH) // 100

    def __str__(self):
        return f"{self.type:<32} {self.rarity_string} owner: {self.owner_id}"

    def __repr__(self):
        return f"Item({self.id=}, {self.type=}, {self.owner_id=}, {self._rarity=}, {self.creation_date=})"

    @property
    def to_database(self) -> tuple[int, str, float, int | None]:
        return self._id, self.type, self._rarity, self.owner_id

    @classmethod
    def from_database(cls, data: tuple[int, str, float, int | None]):
        return cls(*data)
