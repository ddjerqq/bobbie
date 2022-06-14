import disnake
from disnake.ext import commands
from disnake.ext.commands import errors
from disnake import ApplicationCommandInteraction as Aci

from client.client import Client, GUILD_IDS, DEV_TEST
from client.logger import LogLevel
from cogs._cog_services._job_service import JobService


class Jobs(commands.Cog):
    def __init__(self, client: Client):
        self.client = client
        self.job_service     = JobService(client)

    # region COMMAND ROB
    @commands.slash_command(name="rob", guild_ids=GUILD_IDS, description="გაძარცვე ვინმე, ან მოკვდი მცდელობისას")
    @commands.cooldown(1, 300 if not DEV_TEST else 1, commands.BucketType.user)
    async def rob_slash(self, inter: Aci, target: disnake.Member):
        em = await self.job_service.rob(inter.author, target)
        await inter.send(embed=em)

    @commands.command(name="rob")
    @commands.cooldown(1, 300 if not DEV_TEST else 1, commands.BucketType.user)
    async def rob_text(self, ctx: commands.Context, target: disnake.Member):
        em = await self.job_service.rob(ctx.author, target)
        await ctx.send(embed=em)
    # endregion

    # region COMMAND WORK
    @commands.slash_command(name="work", guild_ids=GUILD_IDS, description="იმუშავე და გააკეთე 300 ₾არი")
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def work_slash(self, inter: Aci):
        em = await self.job_service.work(inter.author)
        await inter.send(embed=em)



    @commands.command(name="work")
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def work_text(self, ctx: commands.Context):
        em = await self.job_service.work(ctx.author)
        await ctx.send(embed=em)
    # endregion


def setup(client):
    client.add_cog(Jobs(client))

