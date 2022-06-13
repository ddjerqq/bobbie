
import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction as Aci

from client.client import Client, GUILD_IDS
from cogs.cog_services._economy_service import EconomyService
from cogs.cog_services._job_service import JobService


class Economy(commands.Cog):
    def __init__(self, client: Client):
        self.client = client
        self.economy_service = EconomyService(client)
        self.job_service     = JobService(client)

    @commands.user_command(name="balance", guild_ids=GUILD_IDS, description="user-ის ბალანსი")
    async def balance_user(self, inter: Aci, target: disnake.Member):
        em = await self.economy_service.balance(target)
        await inter.send(embed=em)


    @commands.slash_command(name="balance", guild_ids=GUILD_IDS, description="გაიგე რამდენი ფული გაქვს")
    async def balance_slash(self, inter: Aci, target: disnake.Member = None):
        em = await self.economy_service.balance(target or inter.author)
        await inter.send(embed=em)


    @commands.command(name="balance")
    async def balance_text(self, ctx: commands.Context, target: disnake.Member = None):
        em = await self.economy_service.balance(target or ctx.author)
        await ctx.send(embed=em)

    @commands.slash_command(name="deposit", guild_ids=GUILD_IDS, description="შეიტანე ფული შენი ბანკის აქაუნთში")
    async def deposit(self, inter: Aci, amount: str):
        em = await self.economy_service.deposit(inter.author, amount)
        await inter.send(embed=em)

    @commands.command(name="deposit")
    async def deposit_text(self, ctx: commands.Context, amount: str):
        em = await self.economy_service.deposit(ctx.author, amount)
        await ctx.send(embed=em)


    @commands.slash_command(name="withdraw", guild_ids=GUILD_IDS, description="გამოიტანე ფული ბანკიდან საფულეში")
    async def withdraw(self, inter: Aci, amount: str):
        em = await self.economy_service.withdraw(inter.author, amount)
        await inter.send(embed=em)

    @commands.command(name="withdraw")
    async def withdraw_text(self, ctx: commands.Context, amount: str):
        em = await self.economy_service.withdraw(ctx.author, amount)
        await ctx.send(embed=em)


    @commands.slash_command(name="give", guild_ids=GUILD_IDS, description="მიეც გლახაკთა საჭურჭლე, ათავისუფლე მონები")
    async def give(self, inter: Aci, target: disnake.Member, amount: str):
        await self.economy_service.give(inter, inter.author, target, amount)


    @commands.command(name="give")
    async def give_text(self, ctx: commands.Context, target: disnake.Member, amount: str):
        await self.economy_service.give(ctx, ctx.author, target, amount)


    @commands.slash_command(name="leaderboards", guild_ids=GUILD_IDS, description="Top 10 users")
    async def leaderboards_slash(self, inter: Aci):
        em = await self.client.embeds.economy.leaderboards()
        await inter.send(embed=em)


    @commands.command(name="leaderboards")
    async def leaderboards_text(self, ctx: commands.Context):
        em = await self.client.embeds.economy.leaderboards()
        await ctx.send(embed=em)


def setup(client):
    client.add_cog(Economy(client))
