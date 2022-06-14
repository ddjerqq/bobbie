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
    DISCORD_KITTEN = "DISCORD_KITTEN"
    HAMSTER   = "HAMSTER"


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
    DISCORD_KITTEN = "🐈👧"
    HAMSTER   = "🐀"


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
    DISCORD_KITTEN = "დისკორდ კიტქნი"
    HAMSTER   = "ზაზუნა"


class PetPrice(Enum):
    DOG       = 100
    CAT       = 200
    BIRD      = 300
    CHAMELEON = 400
    PENGUIN   = 500
    WOLF      = 600
    TIGER     = 700
    LION      = 400
    CACTUS    = 500
    BIRD_FISH = 1000
    BANANA    = 1100
    DISCORD_KITTEN = 1200
    HAMSTER   = 200


class PetThumbnail(Enum):
    ...
