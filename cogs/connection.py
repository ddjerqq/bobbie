import discord
from discord.ext import commands

import app


class Connection(commands.Cog):

    def __init__(self, app):
        self.app = app

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bobbie succesfully connected.")
        activity = discord.Game("discord.gg/georgia")
        status = discord.Status.dnd
        await app.app.change_presence(activity=activity, status=status)


def setup(app):
    app.add_cog(Connection(app))
