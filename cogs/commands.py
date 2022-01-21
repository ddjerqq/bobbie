import discord
from discord.ext import commands


class Commands(commands.Cog):

    def __init(self, app):
        self.app = app


def setup(app):
    app.add_cog(Commands(app))
