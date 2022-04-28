import disnake
from disnake.ext import commands
from disnake.ext.commands import errors
from disnake import ApplicationCommandInteraction as Aci

from utils import *
from client import Client
from database.models.item import Item


class InventorySystemCommands(commands.Cog):
    def __init__(self, client: Client):
        self.client = client


    @commands.slash_command(name="buy", guild_ids=GUILD_IDS, description="იყიდე რაიმე ნივთი მაღაზიიდან")
    @commands.cooldown(3, 600 if not DEV_TEST else 1, commands.BucketType.user)
    async def buy(self, inter: Aci, item: Item.tool_buy_prices()):
        user = await self.client.db.users.get(inter.author.id)
        item = Item.new(item)
        price = Item.PRICES[item.type]

        if user.wallet + user.bank < price:
            em = self.client.embeds.econ_err_not_enough_money("რათა", f"იყიდო {item.name}", price)
            await inter.send(embed=em)
            return

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
        em = self.client.embeds.inv_success_bought_item(item)
        await inter.send(embed=em)

    @buy.error
    async def _buy_error(self, ctx: commands.Context, _error: errors.CommandError):
        if isinstance(_error, errors.CommandOnCooldown):
            em = self.client.embeds.cooldown("იყიდე სამი ნივთი მაღაზიიდან", "ყიდვას", _error.retry_after)
            await ctx.send(embed=em)
        else:
            await self.client.log(_error, priority=1)


    @commands.slash_command(name="inventory", guild_ids=GUILD_IDS, description="ნახე შენი ინვენტარი")
    async def inventory(self, inter: Aci):
        em = await self.client.embeds.inv_util_inventory(inter.author)
        await inter.send(embed=em)

    async def _use(self, inter: Aci, item_type: str) -> bool:
        """use item, return True on success, False on unused item"""
        user = await self.client.db.users.get(inter.author.id)
        items = user.items
        tools = list(filter(lambda x: x.type == item_type, items))
        tools.sort(key=lambda x: x.rarity, reverse=True)

        if not len(tools):
            em = self.client.embeds.inv_err_item_not_in_inventory(item_type)
            await inter.send(embed=em)
            return False

        tool = tools[-1]

        if tool.will_break:
            user.items.remove(tool)

        item = Item.random_item(item_type)
        item.owner_id = inter.author.id
        user.experience += 3
        user.items.append(item)

        await self.client.db.users.update(user)

        match tool.type:
            case "fishing_rod":
                em = self.client.embeds.fish(item, tool.will_break)
            case "shovel":
                em = self.client.embeds.dig(item, tool.will_break)
            case "hunting_rifle":
                em = self.client.embeds.hunt(item, tool.will_break)
            case _:
                em = disnake.Embed(title="ამ მაგალითის გამოყენება ვერ მოხერხდა", color=0xFF0000)
                await self.client.log(f"{inter.author.id} tried to use {item_type}", priority=1)
        await inter.send(embed=em)
        return True

    @commands.slash_command(name="fish", guild_ids=GUILD_IDS,
                            description="წადი სათევზაოდ, იქნებ თევზმა ჩაგითრიოს და დაიხრჩო")
    @commands.cooldown(1, 300 if not DEV_TEST else 1, commands.BucketType.user)
    async def fish(self, inter: Aci):
        res = await self._use(inter, "fishing_rod")
        if not res:
            self.fish.reset_cooldown(inter)

    @fish.error
    async def _fish_error(self, ctx: commands.Context, _error: errors.CommandError):
        if isinstance(_error, errors.CommandOnCooldown):
            em = self.client.embeds.cooldown("ითევზავე", "თევზაობას", _error.retry_after)
            await ctx.send(embed=em)
        else:
            await self.client.log(f"{_error}\n{_error.args}", priority=1)

    @commands.slash_command(name="hunt", guild_ids=GUILD_IDS, description="წადი სანადიროდ და შეეცადე შენი თავი არჩინო")
    @commands.cooldown(1, 300 if not DEV_TEST else 1, commands.BucketType.user)
    async def hunt(self, inter: Aci):
        res = await self._use(inter, "hunting_rifle")
        if not res:
            self.hunt.reset_cooldown(inter)

    @hunt.error
    async def _hunt_error(self, ctx: commands.Context, _error: errors.CommandError):
        if isinstance(_error, errors.CommandOnCooldown):
            em = self.client.embeds.cooldown("ინადირე", "ნადირობას", _error.retry_after)
            await ctx.send(embed=em)
        else:
            await self.client.log(f"{_error}\n{_error.args}", priority=1)

    @commands.slash_command(name="dig", guild_ids=GUILD_IDS, description="გათხარე მიწა")
    @commands.cooldown(1, 300 if not DEV_TEST else 1, commands.BucketType.user)
    async def dig(self, inter: Aci):
        res = await self._use(inter, "shovel")
        if not res:
            self.dig.reset_cooldown(inter)

    @dig.error
    async def _dig_error(self, ctx: commands.Context, _error: errors.CommandError):
        if isinstance(_error, errors.CommandOnCooldown):
            em = self.client.embeds.cooldown("გათხარე მიწა", "მიწის გათხრას", _error.retry_after)
            await ctx.send(embed=em)
        else:
            await self.client.log(f"{_error}\n{_error.args}", priority=1)


    @commands.slash_command(name="sell", guild_ids=GUILD_IDS, description="გაყიდე რაიმე ნივთი")
    async def sell(self, inter: Aci, item_type: Item.item_sell_prices(), amount: str = "1"):
        user = await self.client.db.users.get(inter.author.id)
        items = user.items
        items = sorted(filter(lambda x: x.type == item_type, items),
                       key=lambda x: x.rarity, reverse=True)

        if not items:
            em = self.client.embeds.inv_err_item_not_in_inventory(item_type)
            await inter.send(embed=em)
            return

        if amount.isnumeric() and int(amount):
            amount = int(amount)
        elif amount in ["max", "all", "სულ"]:
            amount = len(items)
        else:
            em = self.client.embeds.err_invalid_amount()
            await inter.send(embed=em)
            return

        if amount > len(items):
            em = self.client.embeds.inv_err_not_enough_items(item_type, amount, len(items))
            await inter.send(embed=em)
            return

        total_price = 0
        for idx in range(amount):
            total_price += items[idx].price
            user.items.remove(items[idx])

        user.wallet     += total_price
        user.experience += 3 * amount
        await self.client.db.users.update(user)

        em = self.client.embeds.inv_success_sold_item(item_type, amount, total_price)
        await inter.send(embed=em)

        em = await self.client.embeds.econ_util_balance(inter.author, show_bank=True)
        await inter.send(embed=em)

    @commands.slash_command(name="sell_all", guild_ids=GUILD_IDS, description="გაყიდე ყველაფერი რაც გასაყიდი გაქვს")
    async def sell_all(self, inter: Aci):
        user = await self.client.db.users.get(inter.author.id)
        items = user.items
        items = list(filter(lambda i: not i.buyable, items))

        if not items:
            em = self.client.embeds.inv_err_not_enough_items("გასაყიდი", "ნივთები", "0 ნივთი")
            await inter.send(embed=em)
            return

        confirmation_em = self.client.embeds.confirmation_needed("ყველა ნივთის გაყიდვა?")
        confirmation = self.client.button_service.YesNoButton(intended_user=inter.author)
        await inter.send(embed=confirmation_em, view=confirmation)
        await confirmation.wait()

        if not confirmation.choice:
            cancelled = self.client.embeds.cancelled("შენ გააუქმე ყველა ნივთის გაყიდვა")
            await inter.edit_original_message(embed=cancelled, view=None)
            return

        total_price = 0
        for item in items:
            total_price += item.price
            user.items.remove(item)

        user.experience += 3 * len(items)
        user.wallet += total_price

        await self.client.db.users.update(user)

        em = self.client.embeds.inv_success_sold_all_sellables(len(items), total_price)
        await inter.edit_original_message(embed=em, view=None)

        em = await self.client.embeds.econ_util_balance(inter.author, show_bank=True)
        await inter.send(embed=em)


def setup(client: Client):
    client.add_cog(InventorySystemCommands(client))
