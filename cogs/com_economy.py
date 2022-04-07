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

        user = await self.client.db.user_service.get(target.id)

        embed = disnake.Embed(
            title = f"{target.name}'ს ბალანსი",
            color = 0x2d56a9)

        embed.set_thumbnail(url = target.avatar.url)

        embed.add_field(
            name = "ბანკი",
            value = f"{user.bank}")

        embed.add_field(
            name = "საფულე",
            value = f"{user.wallet}")

        await inter.send(embed = embed)


    @commands.slash_command(name="deposit", guild_ids=GUILD_IDS, description="გადარიცხეთ თანხა საფულიდან ბანკში")
    async def deposit(self, inter: Aci, amount: int):
        success = disnake.Embed(color=0x00ff00, title="წარმატებით შეიტანე ბანკში თანხა")
        fail    = disnake.Embed(color=0xff0000, title="თანხა ვერ შეტანა",
                                description="სავარაუდოდ საფულეში არ გაქვს საკმარისი ფული გიდევს")

        this = await self.client.db.user_service.get(inter.author.id)

        if this.wallet >= amount:
            """success"""
            this.wallet -= amount
            this.bank   += amount
            await self.client.db.user_service.update(this)
            await inter.send(embed=success)

        else:
            """fail"""
            await inter.send(embed=fail)


    @commands.slash_command(name = "withdraw", guild_ids = GUILD_IDS, description = "გამოიტანე ფული ბანკიდან საფულეში")
    async def withdraw(self, inter: Aci, amount: int):
        success = disnake.Embed(color = 0x00ff00, title = "წარმატებით გამოიტანე თანხა ბანკიდან")
        fail = disnake.Embed(color = 0xff0000, title = "თანხა ვერ გამოიტანე მოხერხდა",
                             description = "სავარაუდოდ ბანკში არ გიდევს საკმარისი ფული გაქვს")

        this = await self.client.db.user_service.get(inter.author.id)

        if this.bank >= amount:
            this.bank   -= amount
            this.wallet += amount
            await self.client.db.user_service.update(this)
            await inter.send(embed = success)

        else:
            await inter.send(embed = fail)


    @commands.slash_command(name="give", guild_ids=GUILD_IDS, description="მიეც გლახაკთა საჭურჭლე, ათავისუფლე მონები")
    async def give(self, inter: Aci, target: disnake.Member, amount: int):
        success = disnake.Embed(color = 0x00ff00, title = f"წარმატებით მიეცი {target.name}'ს {amount} ₾")
        fail = disnake.Embed(color = 0xff0000, title = f"შენ ვერ მისცემ {target.name}'ს {amount} ₾ს",
                             description = "სავარაუდოდ ჯიბეში არასაკმარისი ფული გიდევს")
        not_found = disnake.Embed(color = 0xff0000, title = f"{target.name} არ არსებობს?????")
        same_user = disnake.Embed(color = 0xff0000, title = f"შიგ ხოარაგაქვს, ფულს ვის აძლევ??")

        this  = await self.client.db.user_service.get(inter.author.id)
        other = await self.client.db.user_service.get(target.id)

        if this == other:
            await inter.send(embed=same_user)

        elif other is None:
            await inter.send(embed=not_found)

        elif this.wallet >= amount:
            this.wallet  -= amount
            other.wallet += amount
            await self.client.db.user_service.update(this)
            await self.client.db.user_service.update(other)
            await inter.send(embed=success)

        else:
            await inter.send(embed=fail)


    @commands.slash_command(name="rob", guild_ids=GUILD_IDS, description="გაძარცვე ვინმე, ან მოკვდი მცდელობისას")
    @commands.cooldown(1, 300, commands.BucketType.user)
    async def rob(self, inter: Aci, target: disnake.Member):
        success = disnake.Embed(color=0x00ff00, title=f"წარმატებით გაძარცვე {target.name}")
        died    = disnake.Embed(color=0xff0000, title=f"შენ მოკვდი {target.name}'ის ძარცვის დროს 🤣",
                                description=f"შენი საფულე გადაეცა {target.name}'ს")
        not_found = disnake.Embed(color = 0xff0000, title = f"{target.name} არ არსებობს?????")
        same_user = disnake.Embed(color = 0xff0000, title = f"შიგ ხოარაგაქვს, ვის ძარცვავ??")
        no_money  = disnake.Embed(color = 0xff0000, title = f"{target.name}'ს ჯიბეში კაპეიკი არ უდევს",
                                  description = f"მგონი პირიქით იქით უნდა აძლევდე ფულს 🤔")

        this = await self.client.db.user_service.get(inter.author.id)
        other = await self.client.db.user_service.get(target.id)

        if other is None:
            await inter.send(embed=not_found)

        elif this == other:
            await inter.send(embed=same_user)

        elif other.wallet <= 10:
            await inter.send(embed=no_money)

        elif not random.randint(0, 10):
            other.wallet += this.wallet
            this.wallet   = 0
            await inter.send(embed=died)
            await self.client.db.user_service.update(this)
            await self.client.db.user_service.update(other)

        else:
            steal_percentage = random.randint(3, 10)
            steal_amount  = int(other.wallet // steal_percentage)
            this.wallet  += steal_amount
            other.wallet -= steal_amount
            await self.client.db.user_service.update(other)
            await self.client.db.user_service.update(this)
            success.description = f"შენ წარმატებულად მოპარე {other.username}'ს {steal_amount} ₾არი"
            await inter.send(embed=success)


    @rob.error
    async def _rob_error(self, ctx: commands.Context, _error: errors.CommandError):
        if isinstance(_error, errors.CommandOnCooldown):
            embed = disnake.Embed(
                title=f"ნელა ზვიადი", color=0xFF0000,
                description=f"შენ უკვე გაძარცვე ვიღაცა ბოლო ხუთი წუთის განმავლობაში, "
                            f"შენ ისევ შეძლებ ქურდობას {round(_error.retry_after // 60)} წუთში")
            await ctx.send(embed=embed)
        else:
            await self.client.log(_error, priority=1)


    @commands.slash_command(name="work", guild_ids=GUILD_IDS, description="იმუშავე და გააკეთე 100 ₾არი")
    @commands.cooldown(1, 3600, commands.BucketType.user)
    async def work(self, inter: Aci):
        user = await self.client.db.user_service.get(inter.author.id)
        user.experience += 1
        user.wallet     += 100
        await self.client.db.user_service.update(user)
        await inter.send("> შენ იმუშავე და გააკეთე 10 ₾არი <:hammercampfire:960423335437680692>")


    @work.error
    async def _work_error(self, ctx: commands.Context, _error: errors.CommandError):
        if isinstance(_error, errors.CommandOnCooldown):
            embed = disnake.Embed(
                title=f"ნელა ზვიადი", color=0xFF0000,
                description=f"შენ უკვე იმუშავე, შენ შეძლებ ისევ მუშაობას {round(_error.retry_after // 60)} წუთში")
            await ctx.send(embed=embed)
        else:
            await self.client.log(_error, priority=1)


def setup(client):
    client.add_cog(Economy(client))
