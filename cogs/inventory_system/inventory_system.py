import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction as Aci
from disnake.ext.commands import Context as Ctx

from client.client import Client, DEV_TEST, GUILD_IDS
from client.logger import LogLevel
from cogs._cog_services._inventory_service import InventoryService
from database.enums import *
from database.factories.item_factory import ItemFactory



class InsufficientFunds(commands.CheckFailure):...
class HasNoItems(commands.CheckFailure):...
class HasNoItemOfType(commands.CheckFailure):
    def __init__(self, item_type: ItemType, amount: int = None):
        self.item_type = item_type
        super().__init__()


async def has_enough_money(inter: Aci) -> bool:
    client: Client = inter.bot  # type: ignore
    item_slug = inter.filled_options["item"]
    item  = ItemFactory.new(ItemType[item_slug])
    price = item.price
    user = await client.db.users.get(inter.author.id)
    if user.wallet + user.bank < price:
        raise InsufficientFunds()
    return True


async def has_any_item(inter: Aci) -> bool:
    client: Client = inter.bot  # type: ignore
    user = await client.db.users.get(inter.author.id)
    if not user.items:
        raise HasNoItems()
    return True


def has_item_of_type(item_type: ItemType):
    async def predicate(inter: Aci) -> bool:
        client: Client = inter.bot  # type: ignore
        user  = await client.db.users.get(inter.author.id)
        if not any(item.type == item_type for item in user.items):
            raise HasNoItemOfType(item_type)
        return True
    return predicate


async def has_enough_items_to_sell(inter: Aci) -> bool:
    client: Client = inter.bot  # type: ignore
    user = await client.db.users.get(inter.author.id)
    item_slug = inter.filled_options["item_type"]
    type_ = ItemType[item_slug]
    if not any(item.type == type_ for item in user.items):
        raise HasNoItemOfType(type_)
    else:
        return True


class InventorySystemCommands(commands.Cog):
    def __init__(self, client: Client):
        self.client = client
        self.inventory_service = InventoryService(client)

    async def cog_slash_command_error(self, inter: Aci, error: Exception) -> bool:
        if isinstance(error, InsufficientFunds):
            em = await self.client.embeds.economy.error_not_enough_money("ამ ნივთის საყიდლად")
            await inter.send(embed=em)
            return True
        elif isinstance(error, HasNoItems):
            em = await self.client.embeds.generic.generic_error(title="შენ არ გაქვს არაფერი ინვენტარში")
            await inter.send(embed=em)
            return True
        elif isinstance(error, HasNoItemOfType):
            em = await self.client.embeds.inventory.error_item_not_in_inventory(error.item_type.name)
            await inter.send(embed=em)
            return True
        else:
            return False

    @commands.slash_command(name="buy_item", guild_ids=GUILD_IDS,
                            description="იყიდე რაიმე ნივთი მაღაზიიდან")
    @commands.cooldown(2, 600 if not DEV_TEST else 1, commands.BucketType.user)
    @commands.check(has_enough_money)
    async def buy(self, inter: Aci, item: TOOL_BUY_PRICES):  # treat item as item slug
        user = await self.client.db.users.get(inter.author.id)
        item = ItemFactory.new(ItemType[item])
        price = ItemPrice[item.type.name].value  # type: int

        user.experience += 3
        item.owner_id = inter.author.id
        user.items.append(item)

        if user.wallet >= price:
            user.wallet -= price
        else:
            price -= user.wallet
            user.wallet = 0
            user.bank -= price

        await self.client.db.users.update(user)
        em = self.client.embeds.inventory.success_bought_item(item)
        await inter.send(embed=em)


    @commands.slash_command(name="item_inventory", guild_ids=GUILD_IDS,
                            description="ნახე შენი ნივთების ინვენტარი")
    @commands.check(has_any_item)
    async def inventory(self, inter: Aci):
        await self.inventory_service.inventory(inter)

    @commands.slash_command(name="fish", guild_ids=GUILD_IDS,
                            description="წადი სათევზაოდ, იქნებ თევზმა ჩაგითრიოს და დაიხრჩო")
    @commands.cooldown(2, 300 if not DEV_TEST else 1, commands.BucketType.user)
    @commands.check(has_item_of_type(ItemType.FISHING_ROD))
    async def fish(self, inter: Aci):
        em = await self.inventory_service.use(inter.author, ItemType.FISHING_ROD)
        await inter.send(embed=em)


    @commands.slash_command(name="hunt", guild_ids=GUILD_IDS,
                            description="წადი სანადიროდ და შეეცადე შენი თავი არჩინო")
    @commands.cooldown(2, 300 if not DEV_TEST else 1, commands.BucketType.user)
    @commands.check(has_item_of_type(ItemType.HUNTING_RIFLE))
    async def hunt(self, inter: Aci):
        em = await self.inventory_service.use(inter.author, ItemType.HUNTING_RIFLE)
        await inter.send(embed=em)


    @commands.slash_command(name="dig", guild_ids=GUILD_IDS,
                            description="გათხარე მიწა")
    @commands.cooldown(2, 300 if not DEV_TEST else 1, commands.BucketType.user)
    @commands.check(has_item_of_type(ItemType.SHOVEL))
    async def dig(self, inter: Aci):
        em = await self.inventory_service.use(inter.author, ItemType.SHOVEL)
        await inter.send(embed=em)


    @commands.slash_command(name="sell", guild_ids=GUILD_IDS,
                            description="გაყიდე რაიმე ნივთი")
    @commands.check(has_enough_items_to_sell)
    async def sell(self, inter: Aci, item_type: ITEM_SELL_PRICES):
        await self.inventory_service.sell_one_or_all(inter, item_type)

    @commands.slash_command(name="sell_all", guild_ids=GUILD_IDS,
                            description="გაყიდე ყველაფერი რაც გასაყიდი გაქვს")
    @commands.check(has_any_item)
    async def sell_all(self, inter: Aci):
        await self.inventory_service.sell_one_or_all(inter, None, all_=True)


def setup(client: Client):
    client.add_cog(InventorySystemCommands(client))
