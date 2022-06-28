from disnake.ext import commands
from disnake import ApplicationCommandInteraction as Aci
from disnake.ext.commands import Context as Ctx

from client.client import Client, DEV_TEST, GUILD_IDS
from client.logger import LogLevel
from cogs._cog_services._inventory_service import InventoryService
from database.enums import *


class InventorySystemCommands(commands.Cog):
    def __init__(self, client: Client):
        self.client = client
        self.inventory_service = InventoryService(client)

    # region COMMAND BUY
    @commands.slash_command(name="buy_item", guild_ids=GUILD_IDS, description="იყიდე რაიმე ნივთი მაღაზიიდან")
    @commands.cooldown(2, 600 if not DEV_TEST else 1, commands.BucketType.user)
    async def buy_slash(self, inter: Aci, item: TOOL_BUY_PRICES):  # treat item as item slug
        em = await self.inventory_service.buy(inter.author, item)
        await inter.send(embed=em)
    # endregion

    # region COMMAND INVENTORY
    @commands.slash_command(name="item_inventory", guild_ids=GUILD_IDS,
                            description="ნახე შენი ნივთების ინვენტარი")
    async def inventory(self, inter: Aci):
        await self.inventory_service.inventory(inter)
    # endregion

    # region COMMAND FISH
    @commands.slash_command(name="fish", guild_ids=GUILD_IDS,
                            description="წადი სათევზაოდ, იქნებ თევზმა ჩაგითრიოს და დაიხრჩო")
    @commands.cooldown(1, 300 if not DEV_TEST else 1, commands.BucketType.user)
    async def fish_slash(self, inter: Aci):
        em, reset = await self.inventory_service.use(inter.author, ItemType.FISHING_ROD)
        if reset:
            self.fish_slash.reset_cooldown(inter)
        await inter.send(embed=em)

    @commands.command(name="fish")
    @commands.cooldown(1, 300 if not DEV_TEST else 1, commands.BucketType.user)
    async def fish_text(self, ctx: Ctx):
        em, reset = await self.inventory_service.use(ctx.author, ItemType.FISHING_ROD)
        if reset:
            self.fish_text.reset_cooldown(ctx)
        await ctx.send(embed=em)
    # endregion

    # region COMMAND HUNT
    @commands.slash_command(name="hunt", guild_ids=GUILD_IDS, description="წადი სანადიროდ და შეეცადე შენი თავი არჩინო")
    @commands.cooldown(1, 300 if not DEV_TEST else 1, commands.BucketType.user)
    async def hunt_slash(self, inter: Aci):
        em, reset = await self.inventory_service.use(inter.author, ItemType.HUNTING_RIFLE)
        if reset:
            self.hunt_slash.reset_cooldown(inter)
        await inter.send(embed=em)


    @commands.command(name="hunt")
    @commands.cooldown(1, 300 if not DEV_TEST else 1, commands.BucketType.user)
    async def hunt_text(self, ctx: Ctx):
        em, reset = await self.inventory_service.use(ctx.author, ItemType.HUNTING_RIFLE)
        if reset:
            self.hunt_text.reset_cooldown(ctx)
        await ctx.send(embed=em)
    # endregion

    # region COMMAND DIG
    @commands.slash_command(name="dig", guild_ids=GUILD_IDS, description="გათხარე მიწა")
    @commands.cooldown(1, 300 if not DEV_TEST else 1, commands.BucketType.user)
    async def dig_slash(self, inter: Aci):
        em, reset = await self.inventory_service.use(inter.author, ItemType.SHOVEL)
        if reset:
            self.dig_slash.reset_cooldown(inter)
        await inter.send(embed=em)


    @commands.command(name="dig")
    @commands.cooldown(1, 300 if not DEV_TEST else 1, commands.BucketType.user)
    async def dig_text(self, ctx: Ctx):
        em, reset = await self.inventory_service.use(ctx.author, ItemType.SHOVEL)
        if reset:
            self.dig_text.reset_cooldown(ctx)
        await ctx.send(embed=em)
    # endregion

    # region COMMAND SELL
    @commands.slash_command(name="sell", guild_ids=GUILD_IDS, description="გაყიდე რაიმე ნივთი")
    async def sell_slash(self, inter: Aci, item_type: ITEM_SELL_PRICES, amount: str = "1"):
        await self.inventory_service.sell(inter, item_type, amount)


    @commands.command(name="sell")
    async def sell_text(self, ctx: Ctx, item_type: ITEM_SELL_PRICES, amount: str = "1"):
        await self.inventory_service.sell(ctx, item_type, amount)

    @commands.slash_command(name="sell_all", guild_ids=GUILD_IDS, description="გაყიდე ყველაფერი რაც გასაყიდი გაქვს")
    async def sell_all(self, inter: Aci):
        await self.inventory_service.sell(inter, None, None, all_=True)

    @commands.command(name="sell_all")
    async def sell_all_text(self, ctx: Ctx):
        await self.inventory_service.sell(ctx, None, None, all_=True)
    # endregion


def setup(client: Client):
    client.add_cog(InventorySystemCommands(client))
