import disnake
from disnake.ext.commands import Context as Ctx
from client.client import Client
from client.logger import LogLevel
from database.enums import *
from database.factories.item_factory import ItemFactory
from disnake import ApplicationCommandInteraction as Inter


class InventoryService:
    def __init__(self, client: Client):
        self.__client = client


    async def inventory(self, inter: Inter) -> None:
        """
        Handle the user's inventory
        """
        await self.__client.pagination.inventory_pages(inter)


    async def use(self, member: disnake.Member, item_slug: ItemType) -> disnake.Embed:
        """
        Use an item
        :param member: user using the item
        :param item_slug: item to use
        :return: (disnake.Embed, and reset bool)
        if the reset bool is True, then the item was not used, cuz the user didn't have it probably,
        so we should return True
        """
        user = await self.__client.db.users.get(member.id)
        items = user.items
        tools = list(filter(lambda x: x.type == item_slug, items))
        tools.sort(key=lambda x: x.rarity.value, reverse=True)
        tool = tools[-1]

        reward, broken = ItemFactory.use(tool)

        reward.owner_id  = user.id
        user.experience += 3
        user.items.append(reward)

        await self.__client.db.users.update(user)

        match tool.type:
            case ItemType.FISHING_ROD:
                em = self.__client.embeds.utils.fish(reward, broken)
            case ItemType.SHOVEL:
                em = self.__client.embeds.utils.dig(reward, broken)
            case ItemType.HUNTING_RIFLE:
                em = self.__client.embeds.utils.hunt(reward, broken)
            case _:
                await self.__client.logger.log(f"{member} tried to use {item_slug} inside inventory_system.use",
                                               level=LogLevel.ERROR)
                return self.__client.embeds.inventory.error_item_not_in_inventory(item_slug.name)

        return em


    async def sell_one_or_all(self, inter: Inter, item_slug: str | None, all_: bool = False) -> None:
        user  = await self.__client.db.users.get(inter.author.id)
        items = user.items
        items = sorted(filter(lambda x: all_ or x.type.value == item_slug, items),
                       key=lambda x: x.rarity.value, reverse=True)

        if all_:
            amount = len(items)
        else:
            amount = 1

        total_price = 0
        for idx in range(amount):
            total_price += items[idx].price
            user.items.remove(items[idx])

        user.wallet += total_price
        user.experience += 3 * amount
        user.experience += round(total_price / 1000)
        await self.__client.db.users.update(user)

        if not all_:
            sold = self.__client.embeds.inventory.success_sold_item(item_slug, amount, total_price)
        else:
            sold = self.__client.embeds.inventory.success_sold_all_sellables(amount, total_price)
        balance = await self.__client.embeds.economy.balance(inter.author)

        await inter.send(embeds=[sold, balance])
