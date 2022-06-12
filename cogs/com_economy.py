import random

import disnake
from disnake.ext import commands
from disnake.ext.commands import errors
from disnake import ApplicationCommandInteraction as Aci

from client import *
from database.factories.item_factory import ItemFactory
from database.models.item import Item


class Economy(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    @commands.slash_command(name="balance", guild_ids=GUILD_IDS, description="გაიგე რამდენი ფული გაქვს")
    async def balance(self, inter: Aci, target: disnake.Member = None):
        target = target or inter.author
        em = await self.client.embeds.econ_util_balance(target, show_bank=inter.author == target)
        await inter.send(embed=em)

    @commands.slash_command(name="deposit", guild_ids=GUILD_IDS, description="შეიტანე ფული შენი ბანკის აქაუნთში")
    async def deposit(self, inter: Aci, amount: str):
        this = await self.client.db.users.get(inter.author.id)

        if amount.isnumeric() and int(amount):
            amount = int(amount)
        elif amount in ["max", "all", "სულ"]:
            amount = this.wallet
        else:
            em = self.client.embeds.err_invalid_amount()
            await inter.send(embed=em)
            return

        if this.wallet >= amount:
            this.wallet -= amount
            this.bank += amount
            await self.client.db.users.update(this)
            em = self.client.embeds.econ_success_deposit(this, amount)

        else:
            em = self.client.embeds.econ_err_not_enough_money("საფულეში", "ბანკში შეტანისთვის", amount)

        await inter.send(embed=em)

    @commands.slash_command(name="withdraw", guild_ids=GUILD_IDS, description="გამოიტანე ფული ბანკიდან საფულეში")
    async def withdraw(self, inter: Aci, amount: str):
        this = await self.client.db.users.get(inter.author.id)

        if amount.isnumeric() and int(amount):
            amount = int(amount)
        elif amount in ["max", "all", "სულ"]:
            amount = this.wallet
        else:
            em = self.client.embeds.err_invalid_amount()
            await inter.send(embed=em)
            return

        if this.bank >= amount:
            this.bank -= amount
            this.wallet += amount
            await self.client.db.users.update(this)
            em = self.client.embeds.econ_success_withdraw(this, amount)

        else:
            em = self.client.embeds.econ_err_not_enough_money("ბანკში", "გამოსატანად", amount)

        await inter.send(embed=em)

    @commands.slash_command(name="give", guild_ids=GUILD_IDS, description="მიეც გლახაკთა საჭურჭლე, ათავისუფლე მონები")
    async def give(self, inter: Aci, target: disnake.Member, amount: int):
        if inter.author == target:
            em = self.client.embeds.econ_err_self_give()
            await inter.send(embed=em)
            return

        this  = await self.client.db.users.get(inter.author.id)
        other = await self.client.db.users.get(target.id)

        if this is None or other is None:
            em = self.client.embeds.econ_err_user_not_found(inter.author.name)
            await inter.send(embed=em)
            return

        if amount == 0:
            em = self.client.embeds.econ_err_zero_give()
            await inter.send(embed=em)
            return

        if this.wallet + this.bank < amount:
            em = self.client.embeds.econ_err_not_enough_money(
                where="რათა",
                _for=f"მიცე {other.username}'ს ფული",
                needs=amount)
            await inter.send(embed=em)
            return

        if amount >= 100:
            em = self.client.embeds.confirmation_needed(f"{target.name}-ისთვის {amount} ₾-ის მიცემა?")
            confirmation = self.client.button_service.YesNoButton(intended_user=inter.author)
            await inter.send(embed=em, view=confirmation)
            await confirmation.wait()

            if not confirmation.choice:
                em = self.client.embeds.cancelled(f"შენ გადაიფიქრე {target.name}'ისთვის {amount} ის მიცემა")
                await inter.edit_original_message(embed=em, view=None)
                return

        if this.wallet >= amount:
            this.wallet -= amount
            other.wallet += amount

        elif this.wallet + this.bank >= amount:
            amount       -= this.wallet
            other.wallet += this.wallet
            this.wallet   = 0
            this.bank    -= amount
            other.wallet += amount

        await self.client.db.users.update(this)
        await self.client.db.users.update(other)

        em = self.client.embeds.econ_success_give(this, other, amount)
        if amount >= 100:
            await inter.edit_original_message(embed=em, view=None)
        else:
            await inter.send(embed=em)

    @commands.slash_command(name="rob", guild_ids=GUILD_IDS, description="გაძარცვე ვინმე, ან მოკვდი მცდელობისას")
    @commands.cooldown(1, 3600 if not DEV_TEST else 1, commands.BucketType.user)
    async def rob(self, inter: Aci, target: disnake.Member):
        this = await self.client.db.users.get(inter.author.id)
        other = await self.client.db.users.get(target.id)
        items = this.items

        if other is None:
            em = self.client.embeds.generic_error(f"მომხმარებელი არ არის მონაცემთა ბაზაში")

        elif this == other:
            em = self.client.embeds.generic_error("შენ ვერ გაძარცვავ შენს თავს")

        elif other.wallet < 10:
            em = self.client.embeds.generic_error(
                f"შენ ვერ გაძარცვავ {target.name}'ს, რადგან მას ჯიბეში კაპეიკი არ უდევს"
            )

        elif not random.randint(0, 10):
            other.wallet += this.wallet
            this.wallet = 0

            await self.client.db.users.update(this)
            await self.client.db.users.update(other)

            em = self.client.embeds.generic_success(
                title=f"შენ მოკვდი {target.name}'ის ძარცვის დროს🤣",
                description=f"შენი საფულე გადაეცა {target.name}'ს"
            )

        elif "knife" in [i.type for i in items]:
            steal_amount = random.randint(other.wallet // 2, other.wallet)
            this.wallet += steal_amount
            other.wallet -= steal_amount
            await self.client.db.users.update(other)
            await self.client.db.users.update(this)

            knife = sorted(items, key=lambda i: i.rarity, reverse=True)[0]

            if knife.will_break:
                this.items.remove(knife)

            em = self.client.embeds.generic_success(
                description=f"**შენ გაძარცვე** {target.mention}\nმას მოპარე {steal_amount}₾"
            )

        else:
            em = self.client.embeds.generic_error(
                f"შენ ცადე {target.name}'ს გაძარცვა, მაგრამ დანის გარეშე მან სახეში გაგილაწუნა და გაიქცა"
            )

        await inter.send(embed=em)

    @rob.error
    async def _rob_error(self, ctx: commands.Context, _error: errors.CommandError):
        if isinstance(_error, errors.CommandOnCooldown):
            em = self.client.embeds.cooldown("გაძარცვე ვიღაცა", "ქურდობას", _error.retry_after)
            await ctx.send(embed=em)
        else:
            await self.client.log(_error, priority=1)

    @commands.slash_command(name="work", guild_ids=GUILD_IDS, description="იმუშავე და გააკეთე 150 ₾არი")
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def work(self, inter: Aci):
        pay = 150

        user = await self.client.db.users.get(inter.author.id)
        user.experience += 1
        user.wallet += pay
        await self.client.db.users.update(user)

        em = disnake.Embed(
            description=f"**წარმატებული დღე!**\nშენ წახვედი სამსახურში და გამოიმუშავე `{pay}` ₾ <:hammercampfire"
                        f":960423335437680692>", color=0x2b693a)
        em.set_footer(text="(არ დაგავიწყდეს ფულის ბანკში შეტანა, ბევრი ქურდი დახეტიალობს გარეთ)")

        await inter.send(embed=em)

    @work.error
    async def _work_error(self, ctx: commands.Context, _error: errors.CommandError):
        if isinstance(_error, errors.CommandOnCooldown):
            em = self.client.embeds.cooldown("იმუშავე", "მუშაობას", _error.retry_after)
            await ctx.send(embed=em)
        else:
            await self.client.log(_error, priority=1)


    @commands.slash_command(name="leaderboards", guild_ids=GUILD_IDS, description="Top 10 users")
    async def leader_boards(self, inter: Aci):
        em = await self.client.embeds.econ_util_leaderboards()
        await inter.send(embed=em)


    @commands.slash_command(name="starter_pack", guild_ids=GUILD_IDS, description="მიიღე დამწყების პეკი")
    async def starter_pack(self, inter: Aci):
        user = await self.client.db.users.get(inter.author.id)

        if user.experience > 50:
            em = self.client.embeds.generic_error("შენ უკვე გაქვს მიღებული დამწყების პეკი")
            await inter.send(embed=em)
            return

        user.bank += random.randint(1_000, 10_000)
        user.experience += 50

        await self.client.db.users.update(user)

        em1 = self.client.embeds.generic_success(title="კეთილი იყოს შენი მოსვლა!",
                                                 description="შენ მიიღე დამწყების პეკი")

        em2 = await self.client.embeds.econ_util_balance(inter.author, show_bank=True)
        await inter.send(embeds=[em1, em2])


def setup(client):
    client.add_cog(Economy(client))
