import discord
import json
import requests as r
from discord.ext import commands


class Utility(commands.Cog):

    def __init__(self, app):
        self.app = app

    @commands.command()
    async def avatar(self, ctx, *, avamember: discord.Member = None):
        avatar = avamember.avatar_url
        try:
            await ctx.send(avatar)
        except AttributeError as e:
            await ctx.send(e)


def setup(app):
    app.add_cog(Utility(app))
