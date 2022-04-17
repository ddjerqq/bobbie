import random

import disnake
from disnake.ext import commands
from disnake.ext.commands import errors
from disnake import ApplicationCommandInteraction as Aci

from utils import *
from models.client import Client


class Economy(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    @commands.slash_command(name="balance", guild_ids=GUILD_IDS, description="გაიგე რამდენი ფული გაქვს")
    async def balance(self, inter: Aci, target: disnake.Member = None):
        target = target or inter.author
        em = await self.client.embed_service.econ_util_balance(target)
        await inter.send(embed=em)

    @commands.slash_command(name="deposit", guild_ids=GUILD_IDS, description="შეიტანე ფული შენი ბანკის აქაუნთში")
    async def deposit(self, inter: Aci, amount: str):
        this = await self.client.db.user_service.get(inter.author.id)

        if amount.isnumeric():
            amount = int(amount)
        elif amount in ["max", "all", "სულ"]:
            amount = this.wallet
        else:
            em = self.client.embed_service.econ_err_invalid_amount()
            await inter.send(embed=em)
            return

        if this.wallet >= amount:
            this.wallet -= amount
            this.bank += amount
            await self.client.db.user_service.update(this)
            em = self.client.embed_service.econ_success_deposit(this, amount)

        else:
            em = self.client.embed_service.econ_err_not_enough_money("საფულეში", "ბანკში შეტანისთვის", amount)

        await inter.send(embed=em)

    @commands.slash_command(name="withdraw", guild_ids=GUILD_IDS, description="გამოიტანე ფული ბანკიდან საფულეში")
    async def withdraw(self, inter: Aci, amount: str):
        this = await self.client.db.user_service.get(inter.author.id)

        if amount.isnumeric():
            amount = int(amount)
        elif amount in ["max", "all", "სულ"]:
            amount = this.wallet
        else:
            em = self.client.embed_service.econ_err_invalid_amount()
            await inter.send(embed=em)
            return

        if this.bank >= amount:
            this.bank -= amount
            this.wallet += amount
            await self.client.db.user_service.update(this)
            em = self.client.embed_service.econ_success_withdraw(this, amount)

        else:
            em = self.client.embed_service.econ_err_not_enough_money("ბანკში", "გამოსატანად", amount)

        await inter.send(embed=em)

    @commands.slash_command(name="give", guild_ids=GUILD_IDS, description="მიეც გლახაკთა საჭურჭლე, ათავისუფლე მონები")
    async def give(self, inter: Aci, target: disnake.Member, amount: int):
        if inter.author == target:
            em = self.client.embed_service.econ_err_self_give()
            await inter.send(embed=em)

        this  = await self.client.db.user_service.get(inter.author.id)
        other = await self.client.db.user_service.get(target.id)

        if this is None or other is None:
            em = self.client.embed_service.econ_err_user_not_found(inter.author.name)
            await inter.send(embed=em)
            return

        if this.wallet + this.bank < amount:
            em = self.client.embed_service.econ_err_not_enough_money(
                where="რათა",
                _for=f"მიცე {other.username}'ს ფული",
                needs=amount)
            await inter.send(embed=em)
            return

        if this.wallet >= amount:
            this.wallet -= amount
            other.wallet += amount
            em = self.client.embed_service.econ_success_give(this, other, amount)

        elif this.wallet + this.bank >= amount:
            amount -= this.wallet
            this.wallet = 0
            this.bank -= amount
            other.wallet = amount
            em = self.client.embed_service.econ_success_give(this, other, amount)

        await self.client.db.user_service.update(this)
        await self.client.db.user_service.update(other)
        await inter.send(embed=em)

    @commands.slash_command(name="rob", guild_ids=GUILD_IDS, description="გაძარცვე ვინმე, ან მოკვდი მცდელობისას")
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def rob(self, inter: Aci, target: disnake.Member):
        this = await self.client.db.user_service.get(inter.author.id)
        other = await self.client.db.user_service.get(target.id)

        if other is None:
            em = self.client.embed_service.rob_err(f"მომხმარებელი არ არის მონაცემთა ბაზაში")

        elif this == other:
            em = self.client.embed_service.rob_err("შენ ვერ გაძარცვავ შენს თავს")

        elif not random.randint(0, 10):
            other.wallet += this.wallet
            this.wallet = 0

            await self.client.db.user_service.update(this)
            await self.client.db.user_service.update(other)

            em = self.client.embed_service.rob_success_died(target)

        else:
            steal_amount = random.randint(other.wallet // 2, other.wallet)
            this.wallet += steal_amount
            other.wallet -= steal_amount
            await self.client.db.user_service.update(other)
            await self.client.db.user_service.update(this)

            em = self.client.embed_service.rob_success(target, steal_amount)

        await inter.send(embed=em)

    @rob.error
    async def _rob_error(self, ctx: commands.Context, _error: errors.CommandError):
        if isinstance(_error, errors.CommandOnCooldown):
            em = self.client.embed_service.cooldown("გაძარცვე ვიღაცა", "ქურდობას", _error.retry_after)
            await ctx.send(embed=em)
        else:
            await self.client.log(_error, priority=1)

    @commands.slash_command(name="work", guild_ids=GUILD_IDS, description="იმუშავე და გააკეთე 10 ₾არი")
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def work(self, inter: Aci):
        pay = 150

        user = await self.client.db.user_service.get(inter.author.id)
        user.experience += 1
        user.wallet += pay
        await self.client.db.user_service.update(user)

        em = disnake.Embed(
            description=f"შენ წახვედი სამსახურში და გამოიმუშავე {pay} ₾ <:hammercampfire:960423335437680692>")

        await inter.send(embed=em)

    @work.error
    async def _work_error(self, ctx: commands.Context, _error: errors.CommandError):
        if isinstance(_error, errors.CommandOnCooldown):
            em = self.client.embed_service.cooldown("იმუშავე", "მუშაობას", _error.retry_after)
            await ctx.send(embed=em)
        else:
            await self.client.log(_error, priority=1)



def setup(client):
    client.add_cog(Economy(client))
