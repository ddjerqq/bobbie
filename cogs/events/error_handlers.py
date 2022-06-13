import disnake
from disnake.ext import commands
from client.client import Client
from client.logger import LogLevel


class ErrorHandlers(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error: commands.CommandError):
        await self.client.logger.log(f"{ctx!r}\n{error!r}", level=LogLevel.ERROR)
        await ctx.send(embed=self.client.embeds.generic.generic_error("დაფიქსირდა შეცდომა"))

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter: disnake.ApplicationCommandInteraction, error: commands.CommandError):
        await self.client.logger.log(f"{inter!r}\n{error!r}", level=LogLevel.ERROR)
        await inter.send(embed=self.client.embeds.generic.generic_error("დაფიქსირდა შეცდომა"))

    @commands.Cog.listener()
    async def on_user_command_error(self, inter: disnake.ApplicationCommandInteraction, error: commands.CommandError):
        await self.client.logger.log(f"{inter!r}\n{error!r}", level=LogLevel.ERROR)
        await inter.send(embed=self.client.embeds.generic.generic_error("დაფიქსირდა შეცდომა"))

    @commands.Cog.listener()
    async def on_message_command_error(self, inter: disnake.ApplicationCommandInteraction, error: commands.CommandError):
        await self.client.logger.log(f"{inter!r}\n{error!r}", level=LogLevel.ERROR)
        await inter.send(embed=self.client.embeds.generic.generic_error("დაფიქსირდა შეცდომა"))


def setup(client: Client):
    client.add_cog(ErrorHandlers(client))
