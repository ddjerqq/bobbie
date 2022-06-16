import disnake
from disnake.ext.commands import errors
from disnake.ext import commands
from client.client import Client
from client.logger import LogLevel

from disnake.ext.commands import CommandError
from disnake.ext.commands import Context as Ctx
from disnake import ApplicationCommandInteraction as Inter


class ErrorHandlers(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    async def error_handler(self, ctx: Ctx | Inter, error: CommandError):
        match type(error):
            case errors.CommandOnCooldown:
                text = f"შენ უკვე გამოიყენე ეს კომანდა, შენ შეძლებ ისე გამოყენებას {int(error.retry_after)} წამში"
            case errors.CommandNotFound:
                return
            case _:
                text = f"უცნობი შეცდომა: {error}"
                await self.client.logger.log(f"{error!r}", level=LogLevel.ERROR)

        await ctx.send(embed=self.client.embeds.generic.generic_error(title="დაფიქსირდა შეცდომა!", description=text))

    @commands.Cog.listener()
    async def on_command_error(self, ctx: Ctx, error: CommandError):
        await self.error_handler(ctx, error)

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter: Inter, error: CommandError):
        await self.error_handler(inter, error)

    @commands.Cog.listener()
    async def on_user_command_error(self, inter: Inter, error: CommandError):
        await self.error_handler(inter, error)

    @commands.Cog.listener()
    async def on_message_command_error(self, inter: Inter, error: CommandError):
        await self.error_handler(inter, error)


def setup(client: Client):
    client.add_cog(ErrorHandlers(client))
