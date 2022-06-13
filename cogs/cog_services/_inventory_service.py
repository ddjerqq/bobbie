import disnake
from disnake.ext.commands import Context as Ctx
from client.client import Client
from client.logger import LogLevel
from database import ItemType
from database.enums import ItemPrice
from database.factories.item_factory import ItemFactory
from disnake import ApplicationCommandInteraction as Aci


class InventoryService:
    def __init__(self, client: Client):
        self.__client = client

    async def buy(self, buyer: disnake.Member, item_slug: str) -> disnake.Embed:
        """
        Buy an item from the shop
        :param buyer: user buying the item
        :param item_slug: item to buy
        :return: disnake.Embed
        """
        user = await self.__client.db.users.get(buyer.id)
        item = ItemFactory.new(ItemType[item_slug])
        price = ItemPrice[item.type.name].value  # type: int

        if user.wallet + user.bank < price:
            return self.__client.embeds.economy.error_not_enough_money(f"რათა იყიდო {item.name}\nშენ გჭირდება {price}")

        user.experience += 3
        item.owner_id = buyer.id
        user.items.append(item)

        if user.wallet >= price:
            user.wallet -= price
        else:
            price -= user.wallet
            user.wallet = 0
            user.bank -= price

        await self.__client.db.users.update(user)
        em = self.__client.embeds.inventory.success_bought_item(item)
        return em

    async def inventory(self, user: disnake.Member) -> disnake.Embed:
        """
        Show user's inventory
        :param user: user to show inventory of
        :return: disnake.Embed
        """
        user = await self.__client.db.users.get(user.id)
        em   = await self.__client.embeds.inventory.util_inventory(user)
        return em

    async def use(self, member: disnake.Member, item_slug: ItemType) -> tuple[disnake.Embed, bool]:
        """
        Use an item
        :param member: user using the item
        :param item_slug: item to use
        :return: (disnake.Embed, and reset bool)
        if the reset bool is True, then the item was not used, cuz the user didnt have it probably,
        so we should return True
        """
        user = await self.__client.db.users.get(member.id)
        items = user.items
        tools = list(filter(lambda x: x.type == item_slug, items))
        tools.sort(key=lambda x: x.rarity.value, reverse=True)

        if not len(tools):
            em = self.__client.embeds.inventory.error_item_not_in_inventory(item_slug.name)
            return em, True

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
                return self.__client.embeds.inventory.error_item_not_in_inventory(item_slug.name), True

        return em, False

    async def sell(self, inter: Aci | Ctx, item_slug: str | None, amount: str | None, all_: bool = False) -> None:
        """
        Sell an item
        :param inter: interaction object
        :param item_slug: item to sell
        :param amount: amount of items to sell
        :param all_: if true, sell all items of this type
        :return: disnake.Embed
        """
        user  = await self.__client.db.users.get(inter.author.id)
        items = user.items
        items = sorted(filter(lambda x: all_ or x.type.value == item_slug, items),
                       key=lambda x: x.rarity.value, reverse=True)

        if not items:
            em = self.__client.embeds.inventory.error_item_not_in_inventory(item_slug)
            await inter.send(embed=em)
            return

        if all_:
            amount = len(items)
        elif amount.isnumeric() and int(amount):
            amount = int(amount)
        elif amount in ["max", "all", "სულ"]:
            amount = len(items)
        else:
            em = self.__client.embeds.economy.error_invalid_amount_entered()
            await inter.send(embed=em)
            return

        if not all_ and amount > len(items):
            em = self.__client.embeds.inventory.error_not_enough_items(item_slug, amount, len(items))
            await inter.send(embed=em)
            return

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
