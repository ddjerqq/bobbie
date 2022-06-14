from enum import Enum


class ItemType(Enum):
    FISHING_ROD   = "FISHING_ROD"
    HUNTING_RIFLE = "HUNTING_RIFLE"
    SHOVEL        = "SHOVEL"
    COMMON_FISH   = "COMMON_FISH"
    RARE_FISH     = "RARE_FISH"
    TROPICAL_FISH = "TROPICAL_FISH"
    SHARK         = "SHARK"
    GOLDEN_FISH   = "GOLDEN_FISH"
    PIG           = "PIG"
    DEER          = "DEER"
    BEAR          = "BEAR"
    WOLF          = "WOLF"
    TIGER         = "TIGER"
    LION          = "LION"
    ELEPHANT      = "ELEPHANT"
    COPPER_COIN   = "COPPER_COIN"
    EMERALD       = "EMERALD"
    RUBY          = "RUBY"
    SAPPHIRE      = "SAPPHIRE"
    AMETHYST      = "AMETHYST"
    DIAMOND       = "DIAMOND"
    KNIFE         = "KNIFE"
    WEDDING_RING  = "WEDDING_RING"


class ItemEmoji(Enum):
    FISHING_ROD   = "<:fishingrod:963895429248999454>"
    HUNTING_RIFLE = "<:huntingrifle:963895472286756945>"
    SHOVEL        = "<:shovel:964200167001686016>"
    COMMON_FISH   = "<:common_fish:964635049859371049>"
    RARE_FISH     = "<:rare_fish:964635026534842418>"
    TROPICAL_FISH = "<:tropical_fish_:964634994742005770>"
    SHARK         = "<:shark_:964635075922759680>"
    GOLDEN_FISH   = "<:golden_fish:964514375027286056>"
    PIG           = "<:pig_:965295197586079774>"
    DEER          = "<:deer_:965295197783203870>"
    WOLF          = "<:wolf_:964201606763651112>"
    BEAR          = "<:bear_:965304095546150962>"
    LION          = "<:lion_:965363845075980308>"
    COPPER_COIN   = "<:copper_coin_:967416432918933537>"
    RUBY          = "<:ruby_:965920123481358376>"
    SAPPHIRE      = "<:sapphire_:965920195577253888>"
    ELEPHANT      = "<:elephant_:967783490626134016>"
    AMETHYST      = "<:amethyst_:965922934369681448>"


class ItemName(Enum):
    FISHING_ROD   = "ანკესი"
    HUNTING_RIFLE = "სანადირო თოფი"
    SHOVEL        = "ნიჩაბი"
    COMMON_FISH   = "უბრალო თევზი"
    RARE_FISH     = "წითელი თევზი"
    TROPICAL_FISH = "ტროპიკული თევზი"
    SHARK         = "ზვიგენი"
    GOLDEN_FISH   = "ოქროს თევზი"
    PIG           = "გოჭი"
    DEER          = "ირემი"
    BEAR          = "დათვი"
    WOLF          = "მგელი"
    TIGER         = "ვეფხვი"
    LION          = "ლომი"
    ELEPHANT      = "სპილო"
    COPPER_COIN   = "სპილენძის მონეტა"
    EMERALD       = "ზურმუხტი"
    RUBY          = "ლალი"
    SAPPHIRE      = "ფირუზი"
    AMETHYST      = "ამეთვისტო"
    DIAMOND       = "ბრილიანი"
    KNIFE         = "დანა"
    WEDDING_RING  = "საქორწინო ბეჭედი"


class ItemPrice(Enum):
    FISHING_ROD   = 15
    COMMON_FISH   = 5
    RARE_FISH     = 10
    TROPICAL_FISH = 20
    SHARK         = 40
    GOLDEN_FISH   = 50
    HUNTING_RIFLE = 20
    PIG           = 5
    DEER          = 10
    BEAR          = 20
    WOLF          = 30
    TIGER         = 40
    LION          = 50
    ELEPHANT      = 60
    SHOVEL        = 15
    COPPER_COIN   = 1
    EMERALD       = 10
    RUBY          = 20
    SAPPHIRE      = 30
    AMETHYST      = 40
    DIAMOND       = 50
    KNIFE         = 50
    WEDDING_RING  = 500


class ItemThumbnail(Enum):
    FISHING_ROD   = "https://i.imgur.com/m7HBPHl.png"
    HUNTING_RIFLE = "https://i.imgur.com/pjtWTSg.png"
    SHOVEL        = "https://i.imgur.com/Dod0FE4.png"
    COMMON_FISH   = "https://i.imgur.com/I3jU3p7.png"
    RARE_FISH     = "https://i.imgur.com/7f90E9p.png"
    TROPICAL_FISH = "https://i.imgur.com/ZBVZRXw.png"
    SHARK         = "https://i.imgur.com/NMeTrjK.png"
    GOLDEN_FISH   = "https://i.imgur.com/o2m9RkM.png"
    PIG           = "https://i.imgur.com/v1Qa101.png"
    DEER          = "https://i.imgur.com/fGl3N7s.png"
    WOLF          = "https://i.imgur.com/k0fRgHl.png"
    BEAR          = "https://i.imgur.com/4CryBHi.png"
    LION          = "https://i.imgur.com/FBOyDvA.png"
    COPPER_COIN   = "https://i.imgur.com/BR73e8Q.png"
    ELEPHANT      = "https://i.imgur.com/qchItpk.png"
    RUBY          = "https://i.imgur.com/rqOuL5x.png"
    SAPPHIRE      = "https://i.imgur.com/9zrHNnb.png"
    AMETHYST      = "https://i.imgur.com/cookhhr.png"


class Buyable(Enum):
    FISHING_ROD   = "FISHING_ROD"
    HUNTING_RIFLE = "HUNTING_RIFLE"
    SHOVEL        = "SHOVEL"
    KNIFE         = "KNIFE"
    WEDDING_RING  = "WEDDING_RING"

