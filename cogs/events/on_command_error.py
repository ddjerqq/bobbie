from disnake.ext import commands
from client.client import Client
from client.logger import LogLevel


class OnCommandError(commands.Cog):
    def __init__(self, client: Client):
        self.client = client


    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await self.client.logger.log(f"{ctx!r}\n{error!r}", level=LogLevel.ERROR)


def setup(client: Client):
    client.add_cog(OnCommandError(client))
