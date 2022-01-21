import discord
from discord.ext import commands


class Commands(commands.Cog):

    def __init(self, app):
        self.app = app

    @commands.command()
    async def ping(self, ctx):
        await ctx.send("Pong")


def setup(app):
    app.add_cog(Commands(app))
