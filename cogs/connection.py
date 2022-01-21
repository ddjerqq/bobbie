import discord
from discord.ext import commands


class Connection(commands.Cog):

    def __init__(self, app):
        self.app = app

    @commands.Cog.listener()
    async def on_ready(self):
        print("Claude succesfully connected.")


def setup(app):
    app.add_cog(Connection(app))
