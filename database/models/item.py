from __future__ import annotations

import random
import sqlite3
from datetime import datetime

from disnake.ext.commands import option_enum
from database.models.gio_id import Id


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
        "fishing_rod"   : 15,
        "common_fish"   : 5,
        "rare_fish"     : 10,
        "tropical_fish" : 20,
        "shark"         : 40,
        "golden_fish"   : 50,

        "hunting_rifle" : 20,
        "pig"           : 5,
        "deer"          : 10,
        "bear"          : 20,
        "wolf"          : 30,
        "tiger"         : 40,
        "lion"          : 50,
        "elephant"      : 60,

        "shovel"        : 15,
        "copper_coin"   : 1,
        "emerald"       : 10,
        "ruby"          : 20,
        "sapphire"      : 30,
        "amethyst"      : 40,
        "diamond"       : 50,

        "knife"         : 50,
    }

    _FISHABLE_WEIGHTS = {
        "common_fish": 25,
        "rare_fish": 12,
        "tropical_fish": 6,
        "shark": 3,
        "golden_fish": 2,
    }

    _HUNTABLE_WEIGHTS = {
        "pig": 30,
        "deer": 20,
        "bear": 15,
        "wolf": 10,
        "tiger": 5,
        "lion": 2,
        "elephant": 1,
    }

    _DIGABLE_WEIGHTS = {
        "copper_coin": 30,
        "emerald": 20,
        "ruby": 15,
        "sapphire": 10,
        "amethyst": 5,
        "diamond": 2,
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
        "diamond"       : "ბრილიანი",

        "knife"         : "დანა",
    }

    _THUMBNAILS = {
        "fishing_rod"   : "https://i.imgur.com/m7HBPHl.png",
        "hunting_rifle" : "https://i.imgur.com/pjtWTSg.png",
        "shovel"        : "https://i.imgur.com/Dod0FE4.png",
        "common_fish"   : "https://i.imgur.com/I3jU3p7.png",
        "rare_fish"     : "https://i.imgur.com/7f90E9p.png",
        "tropical_fish" : "https://i.imgur.com/ZBVZRXw.png",
        "shark"         : "https://i.imgur.com/NMeTrjK.png",
        "golden_fish"   : "https://i.imgur.com/o2m9RkM.png",
        "pig"           : "https://i.imgur.com/v1Qa101.png",
        "deer"          : "https://i.imgur.com/fGl3N7s.png",
        "wolf"          : "https://i.imgur.com/k0fRgHl.png",
        "bear"          : "https://i.imgur.com/4CryBHi.png",
        "lion"          : "https://i.imgur.com/FBOyDvA.png",
        "copper_coin"   : "https://i.imgur.com/BR73e8Q.png",
        "elephant"      : "https://i.imgur.com/qchItpk.png",
        "ruby"          : "https://i.imgur.com/rqOuL5x.png",
        "sapphire"      : "https://i.imgur.com/9zrHNnb.png",
        "amethyst"      : "https://i.imgur.com/cookhhr.png",

    }

    _EMOJI = {
        "fishing_rod"   : "<:fishingrod:963895429248999454>",
        "hunting_rifle" : "<:huntingrifle:963895472286756945>",
        "shovel"        : "<:shovel:964200167001686016>",
        "common_fish"   : "<:common_fish:964635049859371049>",
        "rare_fish"     : "<:rare_fish:964635026534842418>",
        "tropical_fish" : "<:tropical_fish_:964634994742005770>",
        "shark"         : "<:shark_:964635075922759680>",
        "golden_fish"   : "<:golden_fish:964514375027286056>",
        "pig"           : "<:pig_:965295197586079774>",
        "deer"          : "<:deer_:965295197783203870>",
        "wolf"          : "<:wolf_:964201606763651112>",
        "bear:"         : "<:bear_:965304095546150962>",
        "lion"          : "<:lion_:965363845075980308>",
        "copper_coin"   : "<:copper_coin_:967416432918933537>",
        "ruby"          : "<:ruby_:965920123481358376>",
        "sapphire"      : "<:sapphire_:965920195577253888>",
        "elephant"      : "<:elephant_:967783490626134016>",
        "bear"          : "<:bear_:965304095546150962>",
        "amethyst:"     : "<:amethyst_:965922934369681448>"
    }

    TOOLS = {"fishing_rod", "hunting_rifle", "shovel", "knife"}

    @classmethod
    def tool_buy_prices(cls):
        return option_enum({
            f"{cls._ITEM_NAMES[t]} {cls.PRICES[t]} ₾": t for t in cls.TOOLS
        })

    @classmethod
    def item_sell_prices(cls):
        return option_enum({
            f"{v} {cls.PRICES.get(k, 'undefined')} ₾": k for k, v in cls._ITEM_NAMES.items()
        })

    def __init__(self, id: int, type: str, rarity: float, owner_id: int | None):
        self.__broken = None  # type: bool | None
        self.__id = id
        self.type = type
        self.__rarity = rarity
        self.owner_id = owner_id

    @classmethod
    def new(cls, type: str) -> Item:
        id = Id.new()
        rarity = random.random() ** 2

        return cls(id, type, rarity, None)

    @property
    def id(self) -> int:
        return self.__id

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
    def emoji_id(self) -> int | None:
        """get the emoji id of this item type, if it is missing, then this will return None"""
        em = self._EMOJI.get(self.type, None)
        if em is not None:
            em = em.split(":")[3]
            em = em.split(">")[0]
            em = int(em)
        return em

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
        if 0.0 <= self.__rarity <= 0.07:
            return "სულ ახალი"
        elif 0.07 < self.__rarity <= 0.15:
            return "მინიმალურად გამოყენებული"
        elif 0.15 < self.__rarity <= 0.38:
            return "ოდნავ გამოყენებული"
        elif 0.38 < self.__rarity <= 0.45:
            return "კარგად ნახმარი"
        elif 0.45 < self.__rarity <= 1.00:
            return "დაგლეჯილი"
        else:
            raise ValueError(f"Invalid rarity: {self.__rarity}")

    @property
    def rarity(self) -> float:
        return self.__rarity

    @property
    def created_at(self) -> datetime:
        """
        get the creation date of Item, using _GIO_EPOCH as the base.
        .strftime("%Y-%m-%d %H:%M:%S")
        :return datetime:
        """
        ts = ((self.id >> 22) + Id.EPOCH) // 100
        return datetime.fromtimestamp(ts)

    @property
    def will_break(self) -> bool:
        """
        try break the item, return True if the item broke
        """
        if self.__broken is None:
            self.__broken = random.random() < self.__rarity ** 2.5
        return self.__broken

    def __hash__(self):
        return hash(self.db)

    def __eq__(self, other):
        return isinstance(other, Item) and self.__id == other.__id

    def __str__(self):
        return f"{self.type:<32} {self.rarity_string} owner: {self.owner_id}"

    def __repr__(self):
        return f"<Item id={self.id} type={self.type} owner={self.owner_id} rarity={self.__rarity}>"

    @property
    def db(self) -> tuple:
        return self.__id, self.type, self.__rarity, self.owner_id

    @classmethod
    def from_db(cls, data: tuple | sqlite3.Row) -> Item:
        return cls(*data)

    @classmethod
    def tool_use_result(cls, tool_type: str) -> Item:
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

        random_type = random.choice(list(group.keys()))

        return cls.new(random_type)

    @classmethod
    def random_item(cls) -> Item:
        """
        generate a random item
        """
        random_type = random.choice(list(cls.PRICES.keys()))
        return cls.new(random_type)