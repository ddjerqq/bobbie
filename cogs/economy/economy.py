import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction as Inter

from client.client import Client, GUILD_IDS
from cogs.economy._economy_service import EconomyService
from database.factories.user_factory import UserFactory


class SelfGive(commands.CheckFailure):...
class TargetBot(commands.CheckFailure):...
class NotEnoughMoney(commands.CheckFailure):...
class InvalidAmount(commands.CheckFailure):...

async def check_target_not_bot(inter: Inter) -> bool:
    if inter.author.bot:
        return False
    target = inter.filled_options.get("target", None)  # type: disnake.Member
    if target and target.bot:
        raise TargetBot()
    return True

async def check_amount_valid(inter: Inter) -> bool:
    amount = inter.filled_options["amount"]  # type: int
    if amount < 1:
        raise InvalidAmount()
    return True

def check_has_enough_money(wallet: bool):
    """
    wallet: True, to check the wallet, False to check the bank
    """
    async def predicate(inter: Inter) -> bool:
        client: Client = inter.bot  # type: ignore
        user = await client.db.users.get(inter.author.id)
        amount = inter.filled_options["amount"]  # type: int

        where = user.wallet if wallet else user.bank
        if where < amount:
            raise NotEnoughMoney()
        return True
    return predicate


class Economy(commands.Cog):
    def __init__(self, client: Client):
        self.client = client
        self.economy_service = EconomyService(client)

    async def cog_before_slash_command_invoke(self, inter: Inter) -> None:
        user = await self.client.db.users.get(inter.author.id)
        if user is None:
            user = UserFactory.new(inter.author.id, inter.author.name)
            await self.client.db.users.add(user)

    async def cog_slash_command_error(self, ctx: commands.Context, error: commands.CommandError) -> bool:
        if isinstance(error, NotEnoughMoney):
            await ctx.send(embed=self.client.embeds.economy.error_not_enough_money())
        elif isinstance(error, InvalidAmount):
            await ctx.send(embed=self.client.embeds.economy.error_invalid_amount_entered())
        elif isinstance(error, SelfGive):
            await ctx.send(embed=self.client.embeds.economy.error_self_give())
        elif isinstance(error, TargetBot):
            await ctx.send(embed=self.client.embeds.economy.error_user_not_found())
        else:
            return False
        return True

    @commands.user_command(name="balance", guild_ids=GUILD_IDS, description="user-ის ბალანსი")
    @commands.check(check_amount_valid)
    @commands.check(check_target_not_bot)
    async def balance_user(self, inter: Inter, target: disnake.Member):
        em = await self.economy_service.balance(target)
        await inter.send(embed=em)

    @commands.slash_command(name="balance", guild_ids=GUILD_IDS, description="გაიგე რამდენი ფული გაქვს")
    @commands.check(check_amount_valid)
    @commands.check(check_target_not_bot)
    async def balance_slash(self, inter: Inter, target: disnake.Member = None):
        em = await self.economy_service.balance(target or inter.author)
        await inter.send(embed=em)

    @commands.slash_command(name="deposit", guild_ids=GUILD_IDS, description="შეიტანე ფული შენი ბანკის აქაუნთში")
    @commands.check(check_has_enough_money(wallet=True))
    @commands.check(check_amount_valid)
    @commands.check(check_target_not_bot)
    async def deposit(self, inter: Inter, amount: int):
        await self.economy_service.deposit(inter.author, amount)
        em = disnake.Embed(title="წარმატებით შეიტანე ბანკში ფული")
        await inter.send(embed=em)

    @commands.slash_command(name="withdraw", guild_ids=GUILD_IDS, description="გამოიტანე ფული ბანკიდან საფულეში")
    @commands.check(check_has_enough_money(wallet=False))
    @commands.check(check_amount_valid)
    @commands.check(check_target_not_bot)
    async def withdraw(self, inter: Inter, amount: int):
        await self.economy_service.withdraw(inter.author, amount)
        em = disnake.Embed(title="წარმატებით გამოიტანე ბანკიდან ფული")
        await inter.send(embed=em)

    @commands.slash_command(name="give", guild_ids=GUILD_IDS, description="მიეც გლახაკთა საჭურჭლე, ათავისუფლე მონები")
    @commands.check(check_amount_valid)
    @commands.check(check_target_not_bot)
    async def give(self, inter: Inter, target: disnake.Member, amount: int):
        await self.economy_service.give(inter.author, target, amount)
        em = disnake.Embed(
            title=f"წარმატებით მიეცი {target.display_name}'ს {amount}₾"
        )
        bal_user   = await self.economy_service.balance(inter.author)
        bal_target = await self.economy_service.balance(target)

        await inter.send(embeds=[em, bal_user, bal_target])

    @give.before_invoke
    async def before_give(self, inter: Inter):
        """
        ensure user has enough in their wallet before giving.
        """
        client: Client = inter.bot  # type: ignore
        user = await client.db.users.get(inter.author.id)
        amount = inter.filled_options["amount"]  # type: int
        target = inter.filled_options["target"]  # type: disnake.Member

        if inter.author.id == target.id:
            raise SelfGive()

        if user.wallet >= amount:
            return
        elif user.wallet + user.bank >= amount:
            user.wallet += amount
            user.bank   -= amount
            await client.db.users.update(user)
            return
        else:
            raise NotEnoughMoney()

    @commands.slash_command(name="leaderboards", guild_ids=GUILD_IDS, description="Top 10 users")
    async def leaderboards_slash(self, inter: Inter):
        em = await self.client.embeds.economy.leaderboards()
        await inter.send(embed=em)


def setup(client):
    client.add_cog(Economy(client))
