import enum


class LevelRanges(enum.Enum):
    CHILD       = range(0,   100)
    ADULT       = range(100, 200)
    ELDER       = range(200, 300)
    PATRIARCH   = range(300, 400)
    GRANDMASTER = range(400, 1000)
    MAX         = range(1000, 100000)


class LevelName(enum.Enum):
    CHILD       = "ბავშვი"
    ADULT       = "მოზარდი"
    ELDER       = "ელდერი"
    PATRIARCH   = "პატრიარქი"
    GRANDMASTER = "გროსმეისტერი"
    MAX         = "დამაქსული"
