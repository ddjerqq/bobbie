from enum import Enum


class HuntableRandomWeight(Enum):
    HUNTING_RIFLE = 0
    PIG           = 30
    DEER          = 20
    BEAR          = 15
    WOLF          = 10
    TIGER         = 5
    LION          = 2
    ELEPHANT      = 1


class FishableRandomWeight(Enum):
    FISHING_ROD   = 0
    COMMON_FISH   = 25
    RARE_FISH     = 12
    TROPICAL_FISH = 6
    SHARK         = 3
    GOLDEN_FISH   = 2


class DigableRandomWeight(Enum):
    SHOVEL      = 0
    COPPER_COIN = 30
    EMERALD     = 20
    RUBY        = 15
    SAPPHIRE    = 10
    AMETHYST    = 5
    DIAMOND     = 2
    KNIFE       = 0

