from __future__ import annotations

import time
import random
from datetime import datetime

import disnake.utils
from disnake.ext.commands import option_enum


# 2004/02/16 10 am
_GIO_EPOCH = 107691120000


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

    PRICES = {
        "fishing_rod"  : 15,
        "common_fish"  : 5,
        "rare_fish"    : 10,
        "tropical_fish": 20,
        "shark"        : 40,
        "golden_fish"  : 50,

        "hunting_rifle": 20,
        "pig"          : 5,
        "deer"         : 10,
        "bear"         : 20,
        "wolf"         : 30,
        "tiger"        : 40,
        "lion"         : 50,
        "elephant"     : 60,

        "shovel"       : 15,
        "copper_coin"  : 1,
        "emerald"      : 10,
        "ruby"         : 20,
        "sapphire"     : 30,
        "amethyst"     : 40,
        "diamond"      : 50,
    }

    _FISHABLE_WEIGHTS = {
        "common_fish"   : 25,
        "rare_fish"     : 12,
        "tropical_fish" : 6,
        "shark"         : 3,
        "golden_fish"   : 2,
    }

    _HUNTABLE_WEIGHTS = {
        "pig"           : 30,
        "deer"          : 20,
        "bear"          : 15,
        "wolf"          : 10,
        "tiger"         : 5,
        "lion"          : 2,
        "elephant"      : 1,
    }

    _DIGABLE_WEIGHTS = {
        "copper_coin"   : 30,
        "emerald"       : 20,
        "ruby"          : 15,
        "sapphire"      : 10,
        "amethyst"      : 5,
        "diamond"       : 2,
    }

    _ITEM_NAMES = {
        "fishing_rod"   : "ანკესი",
        "hunting_rifle" : "სანადირო თოფი",
        "shovel"        : "ნიჩაბი",
        "common_fish"   : "უბრალო თევზი",
        "rare_fish"     : "წითელი თევზი",
        "tropical_fish" : "ტროპიკული თევზი",
        "shark"         : "ზვიგენი",
        "golden_fish"   : "ოქროს თევზი",
        "pig"           : "გოჭი",
        "deer"          : "ირემი",
        "bear"          : "დათვი",
        "wolf"          : "მგელი",
        "tiger"         : "ვეფხვი",
        "lion"          : "ლომი",
        "elephant"      : "სპილო",
        "copper_coin"   : "სპილენძის მონეტა",
        "emerald"       : "ზურმუხტი",
        "ruby"          : "ლალი",
        "sapphire"      : "ფირუზი",
        "amethyst"      : "ამეთვისტო",
        "diamond"       : "ბრილიანი"
    }

    _THUMBNAILS = {
        "fishing_rod"  : "https://i.imgur.com/m7HBPHl.png",
        "hunting_rifle": "https://i.imgur.com/pjtWTSg.png",
        "shovel"       : "https://i.imgur.com/Dod0FE4.png",
        "common_fish"  : "https://i.imgur.com/I3jU3p7.png",
        "rare_fish"    : "https://i.imgur.com/7f90E9p.png",
        "tropical_fish": "https://i.imgur.com/ZBVZRXw.png",
        "shark"        : "https://i.imgur.com/NMeTrjK.png",
        "golden_fish"  : "https://i.imgur.com/o2m9RkM.png",
        "pig"          : "https://i.imgur.com/v1Qa101.png",
        "deer"         : "https://i.imgur.com/fGl3N7s.png",
        "wolf"         : "https://i.imgur.com/k0fRgHl.png",
    }

    _EMOJI = {
        "fishing_rod"   : "<:fishingrod:963895429248999454>",
        "hunting_rifle" : "<:huntingrifle:963895472286756945>",
        "shovel"        : "<:shovel:964200167001686016>",
        "common_fish"   : "<:common_fish:964635049859371049>",
        "rare_fish"     : "<:rare_fish:964635026534842418>",
        "tropical_fish_": "<:tropical_fish_:964634994742005770>",
        "shark"         : "<:shark_:964635075922759680>",
        "golden_fish"   : "<:goldenfish:964514375027286056>",
        "pig"           : "<:pig_:965295197586079774>",
        "deer"          : "<:deer_:965295197783203870>",
        "wolf"          : "<:wolf_:964201606763651112>",
    }

    TOOLS = {"fishing_rod", "hunting_rifle", "shovel"}

    @classmethod
    def tool_buy_prices(cls):
        return option_enum({
            f"{cls._ITEM_NAMES[t]} {cls.PRICES[t]} ₾": t for t in cls.TOOLS
        })

    @classmethod
    def item_sell_prices(cls):
        return option_enum({
            v: k for k, v in cls._ITEM_NAMES.items()
        })

    def __init__(self, id: int, type: str, rarity: float, owner_id: int | None):
        self._id = id
        self.type = type
        self._rarity = rarity
        self.owner_id = owner_id

    @classmethod
    def new(cls, type: str) -> Item:
        """
        Create an item, with a unique id which is generated depending on the timestamp
        and _GIO_EPOCH, which is the author's birth time.
        """
        ts = int(time.time() * 100)
        id = (ts - _GIO_EPOCH) << 22
        rarity = (random.random() ** 1.5)

        return cls(id, type, rarity, None)

    @property
    def id(self) -> int:
        return self._id

    @property
    def price(self) -> int:
        p = self.PRICES.get(self.type, 1)
        p += 1 / self.rarity
        return round(p)

    @property
    def buyable(self):
        """
        :return: bool if the item is in {"fishing_rod", "hunting_rifle", "shovel"}
        """
        return self.type in self.TOOLS

    @property
    def emoji(self) -> str:
        """get the emoji of this item type, if it is missing, then this will return an empty string"""
        return self._EMOJI.get(self.type, "")

    @property
    def thumbnail(self) -> str | None:
        """get the item's thumbnail. if its missing, returns None"""
        return self._THUMBNAILS.get(self.type, None)

    @property
    def name(self) -> str:
        """get the item's name. if its missing, returns an empty string"""
        return self._ITEM_NAMES.get(self.type, "")

    @property
    def rarity_string(self) -> str:
        if 0.0 <= self._rarity <= 0.07:
            return "სულ ახალი"
        elif 0.07 < self._rarity <= 0.15:
            return "მინიმალურად ნახმარი"
        elif 0.15 < self._rarity <= 0.38:
            return "გამოცდილი"
        elif 0.38 < self._rarity <= 0.45:
            return "კარგად ნახმარი"
        elif 0.45 < self._rarity <= 1.00:
            return "დაგლეჯილი"
        else:
            raise ValueError(f"Invalid rarity: {self._rarity}")

    @property
    def rarity(self) -> float:
        return self._rarity

    @property
    def creation_epoch(self) -> int:
        """get the creation date of Item, using _GIO_EPOCH as the base."""
        return ((self.id >> 22) + _GIO_EPOCH) // 100

    @property
    def creation_date(self) -> str:
        """
        get the creation date of Item, using _GIO_EPOCH as the base.
        :return: str in format YY-mm-dd HH:MM:SS
        """
        return datetime.fromtimestamp(self.creation_epoch).strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return f"{self.type:<32} {self.rarity_string} owner: {self.owner_id}"

    def __repr__(self):
        return f"Item({self.id=}, {self.type=}, {self.owner_id=}, {self._rarity=}, {self.creation_epoch=})"

    @property
    def to_database(self) -> tuple[int, str, float, int | None]:
        return self._id, self.type, self._rarity, self.owner_id

    @classmethod
    def from_database(cls, data: tuple[int, str, float, int | None]):
        return cls(*data)

    @classmethod
    def random_item(cls, tool_type: str) -> Item:
        """
        generate a random item from the given type of the tool.
        :param tool_type: the type of the tool which is used to acquire the item
        :return: an item of the given type
        """
        match tool_type:
            case "fishing_rod":
                group = cls._FISHABLE_WEIGHTS
            case "hunting_rifle":
                group = cls._HUNTABLE_WEIGHTS
            case "shovel":
                group = cls._DIGABLE_WEIGHTS
            case _:
                raise ValueError(f"item type '{tool_type}' is not a valid too, must be one of {cls.TOOLS}")

        random_type = random.choices(list(group.keys()),
                                     weights=list(group.values()),
                                     k=1)[0]

        return cls.new(random_type)
