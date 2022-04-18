import random

import disnake
from disnake.ext import commands
from disnake.ext.commands import errors
from disnake import ApplicationCommandInteraction as Aci

from utils import *
from models.client import Client
from models.item import Item


class InventorySystemCommands(commands.Cog):
    def __init__(self, client: Client):
        self.client = client


    @commands.slash_command(name="buy", guild_ids=GUILD_IDS, description="იყიდე რაიმე ნივთი მაღაზიიდან")
    @commands.cooldown(3, 600 if not DEV_TEST else 1, commands.BucketType.user)
    async def buy(self, inter: Aci, item: Item.tool_buy_prices()):

        user = await self.client.db.user_service.get(inter.author.id)
        price = Item.PRICES.get(item)
        item = Item.new(item)

        if user.wallet + user.bank < price:
            em = self.client.embed_service.econ_err_not_enough_money("რათა", f"იყიდო {item.name}", price)
            await inter.send(embed=em)
            return

        user.experience += 3
        item.owner_id = inter.author.id
        await self.client.db.item_service.add(item)

        if user.wallet <= price:
            user.wallet -= price
        elif user.wallet + user.bank <= price:
            price -= user.wallet
            user.wallet = 0
            user.bank -= price

        await self.client.db.user_service.update(user)
        em = self.client.embed_service.inv_success_bought_item(item)
        await inter.send(embed=em)

    @buy.error
    async def _buy_error(self, ctx: commands.Context, _error: errors.CommandError):
        if isinstance(_error, errors.CommandOnCooldown):
            em = self.client.embed_service.cooldown("იყიდე სამი ნივთი მაღაზიიდან", "ყიდვას", _error.retry_after)
            await ctx.send(embed=em)
        else:
            await self.client.log(_error, priority=1)


    @commands.slash_command(name="inventory", guild_ids=GUILD_IDS, description="ნახე შენი ინვენტარი")
    async def inventory(self, inter: Aci):
        em = await self.client.embed_service.inv_util_inventory(inter.author)
        await inter.send(embed=em)

    async def _use(self, inter: Aci, item_type: str):
        items = await self.client.db.item_service.get_all_by_owner_id(inter.author.id)
        tools = list(filter(lambda x: x.type == item_type, items))
        tools = sorted(tools, key=lambda x: x.rarity)

        if len(tools) == 0:
            em = self.client.embed_service.inv_err_item_not_in_inventory(item_type)
            await inter.send(embed=em)
            return

        user = await self.client.db.user_service.get(inter.author.id)

        tool = tools[-1]
        broken = random.random() ** 3 < tool.rarity

        if broken:
            await self.client.db.item_service.delete(tool)

        item = Item.random_item(item_type)
        item.owner_id = inter.author.id
        user.experience += 3

        await self.client.db.user_service.update(user)
        await self.client.db.item_service.add(item)

        match tool.type:
            case "fishing_rod":
                em = self.client.embed_service.fish(item, broken)
            case "shovel":
                em = self.client.embed_service.dig(item, broken)
            case "hunting_rifle":
                em = self.client.embed_service.hunt(item, broken)
            case _:
                em = disnake.Embed(title="ამ მაგალითის გამოყენება ვერ მოხერხდა", color=0xFF0000)
                await self.client.log(f"{inter.author.id} tried to use {item_type}", priority=1)
        await inter.send(embed=em)

    @commands.slash_command(name="fish", guild_ids=GUILD_IDS,
                            description="წადი სათევზაოდ, იქნებ თევზმა ჩაგითრიოს და დაიხრჩო")
    @commands.cooldown(1, 300 if not DEV_TEST else 1, commands.BucketType.user)
    async def fish(self, inter: Aci):
        await self._use(inter, "fishing_rod")

    @fish.error
    async def _fish_error(self, ctx: commands.Context, _error: errors.CommandError):
        if isinstance(_error, errors.CommandOnCooldown):
            em = self.client.embed_service.cooldown("ითევზავე", "თევზაობას", _error.retry_after)
            await ctx.send(embed=em)
        else:
            await self.client.log(f"{_error}\n{_error.args}", priority=1)


    @commands.slash_command(name="hunt", guild_ids=GUILD_IDS, description="წადი სანადიროდ და შეეცადე შენი თავი არჩინო")
    @commands.cooldown(1, 300 if not DEV_TEST else 1, commands.BucketType.user)
    async def hunt(self, inter: Aci):
        await self._use(inter, "hunting_rifle")

    @hunt.error
    async def _hunt_error(self, ctx: commands.Context, _error: errors.CommandError):
        if isinstance(_error, errors.CommandOnCooldown):
            em = self.client.embed_service.cooldown("ინადირე", "ნადირობას", _error.retry_after)
            await ctx.send(embed=em)
        else:
            await self.client.log(f"{_error}\n{_error.args}", priority=1)


    @commands.slash_command(name="dig", guild_ids=GUILD_IDS, description="გათხარე მიწა")
    @commands.cooldown(1, 300 if not DEV_TEST else 1, commands.BucketType.user)
    async def dig(self, inter: Aci):
        await self._use(inter, "shovel")

    @dig.error
    async def _dig_error(self, ctx: commands.Context, _error: errors.CommandError):
        if isinstance(_error, errors.CommandOnCooldown):
            em = self.client.embed_service.cooldown("გათხარე მიწა", "მიწის გათხრას", _error.retry_after)
            await ctx.send(embed=em)
        else:
            await self.client.log(f"{_error}\n{_error.args}", priority=1)


    @commands.slash_command(name="sell", guild_ids=GUILD_IDS, description="გაყიდე რაიმე ნივთი")
    async def sell(self, inter: Aci, item_type: Item.item_sell_prices(), amount: str = "1"):
        user = await self.client.db.user_service.get(inter.author.id)
        items = await self.client.db.item_service.get_all_by_owner_id(user.id)
        items = sorted(filter(lambda x: x.type == item_type, items),
                       key=lambda x: x.rarity, reverse=True)

        if not items:
            em = self.client.embed_service.inv_err_item_not_in_inventory(item_type)
            await inter.send(embed=em)
            return

        if amount.isnumeric():
            amount = int(amount)
        elif amount in ["max", "all", "სულ"]:
            amount = len(items)
        else:
            em = self.client.embed_service.err_invalid_amount()
            await inter.send(embed=em)
            return

        if amount > len(items):
            em = self.client.embed_service.inv_err_not_enough_items(item_type, amount, len(items))
            await inter.send(embed=em)
            return

        total_price = 0
        for idx in range(amount):
            total_price += items[idx].price
            await self.client.db.item_service.delete(items[idx])

        user.wallet     += total_price
        user.experience += 3 * amount
        await self.client.db.user_service.update(user)

        em = self.client.embed_service.inv_success_sold_item(item_type, amount, total_price)
        await inter.send(embed=em)

        em = await self.client.embed_service.econ_util_balance(inter.author)
        await inter.send(embed=em)


    @commands.slash_command(name="sell_all", guild_ids=GUILD_IDS, description="გაყიდე ყველაფერი რაც გასაყიდი გაქვს")
    async def sell_all(self, inter: Aci):
        user = await self.client.db.user_service.get(inter.author.id)
        items = await self.client.db.item_service.get_all_by_owner_id(user.id)
        items = list(filter(lambda i: not i.buyable, items))

        total_price = 0
        for item in items:
            total_price += item.price
            await self.client.db.item_service.delete(item)

        user.experience += 3 * len(items)
        user.wallet += total_price

        await self.client.db.user_service.update(user)

        em = self.client.embed_service.inv_success_sold_all_sellables(len(items), total_price)
        await inter.send(embed=em)

        em = await self.client.embed_service.econ_util_balance(inter.author)
        await inter.send(embed=em)


def setup(client: Client):
    client.add_cog(InventorySystemCommands(client))
