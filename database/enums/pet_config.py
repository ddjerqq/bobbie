from enum import Enum


class PetType(Enum):
    DOG       = "DOG"
    CAT       = "CAT"
    BIRD      = "BIRD"
    CHAMELEON = "CHAMELEON"
    PENGUIN   = "PENGUIN"
    WOLF      = "WOLF"
    TIGER     = "TIGER"
    LION      = "LION"
    CACTUS    = "CACTUS"
    BIRD_FISH = "BIRD_FISH"
    BANANA    = "BANANA"


class PetEmoji(Enum):
    DOG       = "🐶"
    CAT       = "🐱"
    BIRD      = "🐦"
    CHAMELEON = "🐓"
    PENGUIN   = "🐧"
    WOLF      = "🐺"
    TIGER     = "🐯"
    LION      = "🦁"
    CACTUS    = "🌵"
    BIRD_FISH = "🐟"
    BANANA    = "🍌"


class PetName(Enum):
    DOG       = "ძაღლი"
    CAT       = "კატა"
    BIRD      = "ჩიტი"
    CHAMELEON = "ქამელეონი"
    PENGUIN   = "პინგვინი"
    WOLF      = "მგელი"
    TIGER     = "ვეფხი"
    LION      = "ლომი"
    CACTUS    = "კაქტუსი"
    BIRD_FISH = "მფრინავი თევზი"
    BANANA    = "ბანანი"


class PetPrice(Enum):
    DOG       = 100
    CAT       = 200
    BIRD      = 300
    CHAMELEON = 400
    PENGUIN   = 500
    WOLF      = 600
    TIGER     = 700
    LION      = 800
    CACTUS    = 900
    BIRD_FISH = 1000
    BANANA    = 1100


class PetThumbnail(Enum):
    ...
