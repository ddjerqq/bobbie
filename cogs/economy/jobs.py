import disnake
from disnake.ext import commands
from disnake.ext.commands import errors
from disnake import ApplicationCommandInteraction as Aci

from client.client import Client, GUILD_IDS, DEV_TEST
from client.logger import LogLevel
from cogs.economy._job_service import JobService


class Jobs(commands.Cog):
    def __init__(self, client: Client):
        self.client = client
        self.job_service     = JobService(client)

    @commands.slash_command(name="rob", guild_ids=GUILD_IDS, description="გაძარცვე ვინმე, ან მოკვდი მცდელობისას")
    @commands.cooldown(1, 300 if not DEV_TEST else 1, commands.BucketType.user)
    async def rob(self, inter: Aci, target: disnake.Member):
        em = await self.job_service.rob(inter.author, target)
        await inter.send(embed=em)


    @rob.error
    async def _rob_error(self, ctx: commands.Context, _error: errors.CommandError):
        if isinstance(_error, errors.CommandOnCooldown):
            em = self.client.embeds.utils.cooldown("გაძარცვე ვიღაცა", "ქურდობას", _error.retry_after)
            await ctx.send(embed=em)
        else:
            await self.client.logger.log(_error, level=LogLevel.ERROR)


    @commands.slash_command(name="work", guild_ids=GUILD_IDS, description="იმუშავე და გააკეთე 150 ₾არი")
    @commands.cooldown(1, 600, commands.BucketType.user)
    async def work(self, inter: Aci):
        em = await self.job_service.work(inter.author)
        await inter.send(embed=em)


    @work.error
    async def _work_error(self, ctx: commands.Context, _error: errors.CommandError):
        if isinstance(_error, errors.CommandOnCooldown):
            em = self.client.embeds.cooldown("იმუშავე", "მუშაობას", _error.retry_after)
            await ctx.send(embed=em)
        else:
            await self.client.logger.log(_error, level=LogLevel.ERROR)
