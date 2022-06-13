from disnake.ext import commands
from disnake.ext.commands import errors
from disnake import ApplicationCommandInteraction as Aci

from client.client import Client, DEV_TEST, GUILD_IDS
from client.logger import LogLevel
from cogs.inventory_system._inventory_service import InventoryService
from database.enums import *
from database.factories.item_factory import ItemFactory


class InventorySystemCommands(commands.Cog):
    def __init__(self, client: Client):
        self.client = client
        self.inventory_service = InventoryService(client)

    @commands.slash_command(name="buy", guild_ids=GUILD_IDS, description="იყიდე რაიმე ნივთი მაღაზიიდან")
    @commands.cooldown(4, 600 if not DEV_TEST else 1, commands.BucketType.user)
    async def buy(self, inter: Aci, item: TOOL_BUY_PRICES):  # treat item as item slug
        em = await self.inventory_service.buy(inter.author, item)
        await inter.send(embed=em)

    @buy.error
    async def _buy_error(self, ctx: commands.Context, _error: errors.CommandError):
        if isinstance(_error, errors.CommandOnCooldown):
            em = self.client.embeds.cooldown("იყიდე ოთხი ნივთი მაღაზიიდან", "ყიდვას", _error.retry_after)
            await ctx.send(embed=em)
        else:
            await self.client.logger.log(_error, level=LogLevel.ERROR)
            await ctx.send(embed=self.client.embeds.generic.generic_error("დაფიქსირდა შეცდომა",
                                                                          description=str(_error)))

    @commands.slash_command(name="inventory", guild_ids=GUILD_IDS, description="ნახე შენი ინვენტარი")
    async def inventory(self, inter: Aci):
        em = await self.inventory_service.inventory(inter.author)
        await inter.send(embed=em)

    @commands.slash_command(name="fish", guild_ids=GUILD_IDS,
                            description="წადი სათევზაოდ, იქნებ თევზმა ჩაგითრიოს და დაიხრჩო")
    @commands.cooldown(2, 300 if not DEV_TEST else 1, commands.BucketType.user)
    async def fish(self, inter: Aci):
        em, reset = await self.inventory_service.use(inter.author, ItemType.FISHING_ROD)
        if reset:
            self.fish.reset_cooldown(inter)
        else:
            await inter.send(embed=em)

    @fish.error
    async def _fish_error(self, ctx: commands.Context, _error: errors.CommandError):
        if isinstance(_error, errors.CommandOnCooldown):
            em = self.client.embeds.cooldown("ითევზავე", "თევზაობას", _error.retry_after)
            await ctx.send(embed=em)
        else:
            await self.client.logger.log(_error, level=LogLevel.ERROR)
            await ctx.send(embed=self.client.embeds.generic.generic_error("დაფიქსირდა შეცდომა",
                                                                          description=str(_error)))

    @commands.slash_command(name="hunt", guild_ids=GUILD_IDS, description="წადი სანადიროდ და შეეცადე შენი თავი არჩინო")
    @commands.cooldown(3, 300 if not DEV_TEST else 1, commands.BucketType.user)
    async def hunt(self, inter: Aci):
        em, reset = await self.inventory_service.use(inter.author, ItemType.HUNTING_RIFLE)
        if reset:
            self.fish.reset_cooldown(inter)
        else:
            await inter.send(embed=em)

    # @hunt.error
    # async def _hunt_error(self, ctx: commands.Context, _error: errors.CommandError):
    #     if isinstance(_error, errors.CommandOnCooldown):
    #         em = self.client.embeds.cooldown("ინადირე", "ნადირობას", _error.retry_after)
    #         await ctx.send(embed=em)
    #     else:
    #         await self.client.logger.log(_error, level=LogLevel.ERROR)
    #         await ctx.send(embed=self.client.embeds.generic.generic_error("დაფიქსირდა შეცდომა",
    #                                                                       description=str(_error)))

    @commands.slash_command(name="dig", guild_ids=GUILD_IDS, description="გათხარე მიწა")
    @commands.cooldown(3, 300 if not DEV_TEST else 1, commands.BucketType.user)
    async def dig(self, inter: Aci):
        em, reset = await self.inventory_service.use(inter.author, ItemType.SHOVEL)
        if reset:
            self.fish.reset_cooldown(inter)
        else:
            await inter.send(embed=em)

    @dig.error
    async def _dig_error(self, ctx: commands.Context, _error: errors.CommandError):
        if isinstance(_error, errors.CommandOnCooldown):
            em = self.client.embeds.cooldown("გათხარე მიწა", "მიწის გათხრას", _error.retry_after)
            await ctx.send(embed=em)
        else:
            await self.client.logger.log(_error, level=LogLevel.ERROR)
            await ctx.send(embed=self.client.embeds.generic.generic_error("დაფიქსირდა შეცდომა",
                                                                          description=str(_error)))

    @commands.slash_command(name="sell", guild_ids=GUILD_IDS, description="გაყიდე რაიმე ნივთი")
    async def sell(self, inter: Aci, item_type: ITEM_SELL_PRICES, amount: str = "1"):
        await self.inventory_service.sell(inter, item_type, amount)

    @commands.slash_command(name="sell_all", guild_ids=GUILD_IDS, description="გაყიდე ყველაფერი რაც გასაყიდი გაქვს")
    async def sell_all(self, inter: Aci):
        await self.inventory_service.sell(inter, None, None, all_=True)


def setup(client: Client):
    client.add_cog(InventorySystemCommands(client))
