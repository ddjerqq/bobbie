import disnake

from database.enums import *
from database.factories.item_factory import ItemFactory
from database.models.item import Item
from database.models.pet import Pet
from database.models.user import User


class PetEmbedService:
    def __init__(self, client):
        self.__client = client

    async def util_inventory(self, user: User) -> disnake.Embed:
        # FEATURE remake this too
        total_price = sum(item.price for item in user.items)

        em = disnake.Embed(title=f"{user.username}'ის ცხოველები",
                           description=f"{len(user.items)} ცხოველი, სულ `{total_price}`₾", )

        item_types = {pet.type: [] for pet in user.pets}  # type: dict[PetType, list[Pet]]

        for pet in user.pets:
            item_types[pet.type].append(pet)

        for pet_type, pets in item_types.items():
            tot_price = sum(i.price for i in pets)
            total     = len(item_types[pet_type])
            em.add_field(name=f"{pets[0].emoji} {pets[0].name} ─ {total}",
                         value=f"ფასი ჯამში: `{tot_price}`₾")

        # TODO maybe make this prettier later
        # TODO pagination maybe

        return em
