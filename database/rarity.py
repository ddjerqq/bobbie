from __future__ import annotations
import random


class Rarity:
    """
    rarity object with encapsulation.

    Examples:
        >>> r = Rarity.new()
        >>> print(r.name)
        >>> "Factory New"
    """
    def __init__(self, rarity: float):
        self.__rarity = rarity

    @classmethod
    def new(cls) -> Rarity:
        """
        create rarity with this
        :return: Rarity object
        """
        return cls(random.random() ** 2)

    @property
    def value(self):
        return self.__rarity

    @property
    def name(self):
        if 0.0 <= self.__rarity <= 0.07:
            return "სულ ახალი"
        elif 0.07 < self.__rarity <= 0.15:
            return "მინიმალურად გამოყენებული"
        elif 0.15 < self.__rarity <= 0.38:
            return "ოდნავ გამოყენებული"
        elif 0.38 < self.__rarity <= 0.45:
            return "კარგად ნახმარი"
        else:
            return "დაგლეჯილი"

    def __repr__(self):
        return f"<Rarity {self.name} {self.__rarity}>"

    def __str__(self):
        return self.name
