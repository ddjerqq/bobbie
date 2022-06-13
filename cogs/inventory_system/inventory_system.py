from disnake.ext import commands
from disnake.ext.commands import errors
from disnake import ApplicationCommandInteraction as Aci
from disnake.ext.commands import Context as Ctx

from client.client import Client, DEV_TEST, GUILD_IDS
from client.logger import LogLevel
from cogs.cog_services._inventory_service import InventoryService
from database.enums import *


class InventorySystemCommands(commands.Cog):
    def __init__(self, client: Client):
        self.client = client
        self.inventory_service = InventoryService(client)

    # region COMMAND BUY
    @commands.slash_command(name="buy", guild_ids=GUILD_IDS, description="იყიდე რაიმე ნივთი მაღაზიიდან")
    @commands.cooldown(2, 600 if not DEV_TEST else 1, commands.BucketType.user)
    async def buy_slash(self, inter: Aci, item: TOOL_BUY_PRICES):  # treat item as item slug
        em = await self.inventory_service.buy(inter.author, item)
        await inter.send(embed=em)

    @buy_slash.error
    async def _buy_slash_error(self, ctx: commands.Context, _error: errors.CommandError):
        if isinstance(_error, errors.CommandOnCooldown):
            em = self.client.embeds.cooldown("იყიდე ოთხი ნივთი მაღაზიიდან", "ყიდვას", _error.retry_after)
            await ctx.send(embed=em)
        else:
            await self.client.logger.log(_error, level=LogLevel.ERROR)
            await ctx.send(embed=self.client.embeds.generic.generic_error("დაფიქსირდა შეცდომა",
                                                                          description=str(_error)))

    @commands.command(name="buy")
    @commands.cooldown(2, 600 if not DEV_TEST else 1, commands.BucketType.user)
    async def buy_text(self, ctx: Ctx, item: TOOL_BUY_PRICES):
        em = await self.inventory_service.buy(ctx.author, item)
        await ctx.send(embed=em)

    @buy_text.error
    async def _buy_text_error(self, ctx: commands.Context, _error: errors.CommandError):
        if isinstance(_error, errors.CommandOnCooldown):
            em = self.client.embeds.cooldown("იყიდე ოთხი ნივთი მაღაზიიდან", "ყიდვას", _error.retry_after)
            await ctx.send(embed=em)
        else:
            await self.client.logger.log(_error, level=LogLevel.ERROR)
            await ctx.send(embed=self.client.embeds.generic.generic_error("დაფიქსირდა შეცდომა",
                                                                          description=str(_error)))
    # endregion

    # region COMMAND INVENTORY
    @commands.slash_command(name="inventory", guild_ids=GUILD_IDS, description="ნახე შენი ინვენტარი")
    async def inventory(self, inter: Aci):
        em = await self.inventory_service.inventory(inter.author)
        await inter.send(embed=em)

    @commands.command(name="inventory")
    async def inventory_text(self, ctx: Ctx):
        em = await self.inventory_service.inventory(ctx.author)
        await ctx.send(embed=em)
    # endregion

    # region COMMAND FISH
    @commands.slash_command(name="fish", guild_ids=GUILD_IDS,
                            description="წადი სათევზაოდ, იქნებ თევზმა ჩაგითრიოს და დაიხრჩო")
    @commands.cooldown(1, 300 if not DEV_TEST else 1, commands.BucketType.user)
    async def fish_slash(self, inter: Aci):
        em, reset = await self.inventory_service.use(inter.author, ItemType.FISHING_ROD)
        if reset:
            self.fish_slash.reset_cooldown(inter)
        else:
            await inter.send(embed=em)

    @fish_slash.error
    async def _fish_slash_error(self, ctx: commands.Context, _error: errors.CommandError):
        if isinstance(_error, errors.CommandOnCooldown):
            em = self.client.embeds.cooldown("ითევზავე", "თევზაობას", _error.retry_after)
            await ctx.send(embed=em)
        else:
            await self.client.logger.log(_error, level=LogLevel.ERROR)
            await ctx.send(embed=self.client.embeds.generic.generic_error("დაფიქსირდა შეცდომა",
                                                                          description=str(_error)))

    @commands.command(name="fish")
    @commands.cooldown(1, 300 if not DEV_TEST else 1, commands.BucketType.user)
    async def fish_text(self, ctx: Ctx):
        em, reset = await self.inventory_service.use(ctx.author, ItemType.FISHING_ROD)
        if reset:
            self.fish_text.reset_cooldown(ctx)
        else:
            await ctx.send(embed=em)

    @fish_text.error
    async def _fish_text_error(self, ctx: commands.Context, _error: errors.CommandError):
        if isinstance(_error, errors.CommandOnCooldown):
            em = self.client.embeds.cooldown("ითევზავე", "თევზაობას", _error.retry_after)
            await ctx.send(embed=em)
        else:
            await self.client.logger.log(_error, level=LogLevel.ERROR)
            await ctx.send(embed=self.client.embeds.generic.generic_error("დაფიქსირდა შეცდომა",
                                                                          description=str(_error)))
    # endregion

    # region COMMAND HUNT
    @commands.slash_command(name="hunt", guild_ids=GUILD_IDS, description="წადი სანადიროდ და შეეცადე შენი თავი არჩინო")
    @commands.cooldown(1, 300 if not DEV_TEST else 1, commands.BucketType.user)
    async def hunt_slash(self, inter: Aci):
        em, reset = await self.inventory_service.use(inter.author, ItemType.HUNTING_RIFLE)
        if reset:
            self.hunt_slash.reset_cooldown(inter)
        else:
            await inter.send(embed=em)

    @hunt_slash.error
    async def _hunt_error(self, ctx: commands.Context, _error: errors.CommandError):
        if isinstance(_error, errors.CommandOnCooldown):
            em = self.client.embeds.cooldown("ინადირე", "ნადირობას", _error.retry_after)
            await ctx.send(embed=em)
        else:
            await self.client.logger.log(_error, level=LogLevel.ERROR)
            await ctx.send(embed=self.client.embeds.generic.generic_error("დაფიქსირდა შეცდომა",
                                                                          description=str(_error)))


    @commands.command(name="hunt")
    @commands.cooldown(1, 300 if not DEV_TEST else 1, commands.BucketType.user)
    async def hunt_text(self, ctx: Ctx):
        em, reset = await self.inventory_service.use(ctx.author, ItemType.HUNTING_RIFLE)
        if reset:
            self.hunt_text.reset_cooldown(ctx)
        else:
            await ctx.send(embed=em)

    @hunt_text.error
    async def _hunt_error(self, ctx: commands.Context, _error: errors.CommandError):
        if isinstance(_error, errors.CommandOnCooldown):
            em = self.client.embeds.cooldown("ინადირე", "ნადირობას", _error.retry_after)
            await ctx.send(embed=em)
        else:
            await self.client.logger.log(_error, level=LogLevel.ERROR)
            await ctx.send(embed=self.client.embeds.generic.generic_error("დაფიქსირდა შეცდომა",
                                                                          description=str(_error)))
    # endregion

    # region COMMAND DIG
    @commands.slash_command(name="dig", guild_ids=GUILD_IDS, description="გათხარე მიწა")
    @commands.cooldown(1, 300 if not DEV_TEST else 1, commands.BucketType.user)
    async def dig_slash(self, inter: Aci):
        em, reset = await self.inventory_service.use(inter.author, ItemType.SHOVEL)
        if reset:
            self.dig_slash.reset_cooldown(inter)
        else:
            await inter.send(embed=em)

    @dig_slash.error
    async def _dig_slash_error(self, ctx: commands.Context, _error: errors.CommandError):
        if isinstance(_error, errors.CommandOnCooldown):
            em = self.client.embeds.cooldown("გათხარე მიწა", "მიწის გათხრას", _error.retry_after)
            await ctx.send(embed=em)
        else:
            await self.client.logger.log(_error, level=LogLevel.ERROR)
            await ctx.send(embed=self.client.embeds.generic.generic_error("დაფიქსირდა შეცდომა",
                                                                          description=str(_error)))


    @commands.command(name="dig")
    @commands.cooldown(1, 300 if not DEV_TEST else 1, commands.BucketType.user)
    async def dig_text(self, ctx: Ctx):
        em, reset = await self.inventory_service.use(ctx.author, ItemType.SHOVEL)
        if reset:
            self.dig_text.reset_cooldown(ctx)
        else:
            await ctx.send(embed=em)

    @dig_text.error
    async def _dig_text_error(self, ctx: commands.Context, _error: errors.CommandError):
        if isinstance(_error, errors.CommandOnCooldown):
            em = self.client.embeds.cooldown("გათხარე მიწა", "მიწის გათხრას", _error.retry_after)
            await ctx.send(embed=em)
        else:
            await self.client.logger.log(_error, level=LogLevel.ERROR)
            await ctx.send(embed=self.client.embeds.generic.generic_error("დაფიქსირდა შეცდომა",
                                                                          description=str(_error)))
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
