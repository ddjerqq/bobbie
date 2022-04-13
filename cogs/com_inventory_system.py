import random

import disnake
from disnake.ext import commands
from disnake.ext.commands import errors
from disnake import ApplicationCommandInteraction as Aci

from utils import *
from models.client import Client
from models.user import User
from models.item import (Item, ITEMS_AND_PRICES, TOOL_BUY_PRICES,
                         ITEM_ENUM, BUYABLE, FISHES, ANIMALS, DUG_ITEMS)


class InventorySystemCommands(commands.Cog):
    def __init__(self, client: Client):
        self.client = client


    @commands.slash_command(name="buy", guild_ids=GUILD_IDS, description="იყიდე რაიმე ნივთი მაღაზიიდან")
    @commands.cooldown(3, 600, commands.BucketType.user)
    async def buy(self, inter: Aci, item: TOOL_BUY_PRICES):
        if item not in ITEMS_AND_PRICES:
            em = self.client.embed_service.inv_err_item_not_in_shop(item)
            await inter.send(embed=em)
            return

        elif item not in BUYABLE:
            em = self.client.embed_service.inv_err_item_not_buyable(item)
            await inter.send(embed=em)
            return

        price = ITEMS_AND_PRICES[item]
        user = await self.client.db.user_service.get(inter.author.id)

        if user.wallet < price:
            em = self.client.embed_service.econ_err_not_enough_money("ბანკში", f"{item} ის საყიდლად", price)
            await inter.send(embed=em)
            return

        user.wallet -= price
        user.experience += 3
        item = Item.new(item)
        item.owner_id = inter.author.id

        await self.client.db.item_service.add(item)
        await self.client.db.user_service.update(user)

        # await self.client.log(f"({inter.author.id}) {inter.author.name} bought ({item.id}) {item.type}")

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
        items = list(filter(lambda x: x.type == item_type, items))
        items = sorted(items, key=lambda x: x.rarity)

        if not items:
            em = self.client.embed_service.inv_err_item_not_in_inventory(item_type)
            await inter.send(embed=em)
            return

        user = await self.client.db.user_service.get(inter.author.id)

        tool = items[-1]
        broken = random.random() ** 0.2 < tool.rarity

        if broken:
            await self.client.db.item_service.delete(tool.id)

        group = None
        for g in [ANIMALS, FISHES, DUG_ITEMS]:
            if item_type in g:
                group = g
                break

        total_price = sum(group.values())
        item_random_weights = {
            i: total_price // p for i, p in group.items()
        }

        item = random.choices(list(item_random_weights.keys()),
                              weights=list(item_random_weights.values()),
                              k=1)[0]
        item = Item.new(item)
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


    @commands.slash_command(name="fish", guild_ids=GUILD_IDS, description="წადი სათევზაოდ")
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def fish(self, inter: Aci):
        await self._use(inter, "fishing_rod")

    @fish.error
    async def _fish_error(self, ctx: commands.Context, _error: errors.CommandError):
        if isinstance(_error, errors.CommandOnCooldown):
            em = self.client.embed_service.cooldown("ითევზავე", "თევზაობას", _error.retry_after)
            await ctx.send(embed=em)
        else:
            await self.client.log(_error, priority=1)


    @commands.slash_command(name="hunt", guild_ids=GUILD_IDS, description="წადი სანადიროდ")
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def hunt(self, inter: Aci):
        await self._use(inter, "fishing_rod")

    @hunt.error
    async def _hunt_error(self, ctx: commands.Context, _error: errors.CommandError):
        if isinstance(_error, errors.CommandOnCooldown):
            em = self.client.embed_service.cooldown("ინადირე", "ნადირობას", _error.retry_after)
            await ctx.send(embed=em)
        else:
            await self.client.log(_error, priority=1)


    @commands.slash_command(name="dig", guild_ids=GUILD_IDS, description="გათხარე მიწა")
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def dig(self, inter: Aci):
        await self._use(inter, "shovel")

    @dig.error
    async def _dig_error(self, ctx: commands.Context, _error: errors.CommandError):
        if isinstance(_error, errors.CommandOnCooldown):
            em = self.client.embed_service.cooldown("გათხარე მიწა", "მიწის გათხრას", _error.retry_after)
            await ctx.send(embed=em)
        else:
            await self.client.log(_error, priority=1)


    @commands.slash_command(name="sell", guild_ids=GUILD_IDS, description="გაყიდე ნივთი")
    async def sell(self, inter: Aci, item: ITEM_ENUM):
        user = await self.client.db.user_service.get(inter.author.id)
        user_items = await self.client.db.item_service.get_all_by_owner_id(user.id)

        if item not in list(map(lambda x: x.type, user_items)):
            em = self.client.embed_service.inv_err_item_not_in_inventory(item)
            await inter.send(embed=em)
            return

        items = list(filter(lambda x: x.type == item, user_items))
        items = sorted(items, key=lambda x: x.rarity)
        item  = items[-1]

        user.wallet += item.price
        user.experience += 5
        await self.client.db.user_service.update(user)
        await self.client.db.item_service.delete(item)

        em = self.client.embed_service.sell(item)

        await inter.send(embed=em)


def setup(client: Client):
    client.add_cog(InventorySystemCommands(client))
