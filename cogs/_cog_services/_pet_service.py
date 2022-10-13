import disnake
from client.client import Client
from database import PetType, PetPrice
from database.factories.pet_factory import PetFactory


class PetService:
    def __init__(self, client: Client):
        self.__client = client

    async def buy(self, buyer: disnake.Member, pet_slug: str) -> disnake.Embed:
        """
        Buy a pet from the shop
        :param buyer: user buying the item
        :param pet_slug: pet to buy
        :return: disnake.Embed
        """
        user  = await self.__client.db.users.get(buyer.id)
        pet   = PetFactory.new(PetType[pet_slug])
        price = PetPrice[pet_slug].value  # type: int

        if user.wallet + user.bank < price:
            return self.__client.embeds.economy.error_not_enough_money(f"რათა იყიდო {pet.name}\nშენ გჭირდება {price}")

        user.experience += 30
        pet.owner_id = buyer.id
        user.pets.append(pet)

        if user.wallet >= price:
            user.wallet -= price
        else:
            price -= user.wallet
            user.wallet = 0
            user.bank -= price

        await self.__client.db.users.update(user)
        em = self.__client.embeds.inventory.success_bought_item(pet)
        return em


    async def inventory(self, member: disnake.Member) -> disnake.Embed:
        user = await self.__client.db.users.get(member.id)
        em   = await self.__client.embeds.pets.util_inventory(user)
        return em
