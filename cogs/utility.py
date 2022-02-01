import discord
import json
import requests as r
from discord.ext import commands

import app


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

    @commands.command()
    async def say(self, ctx):
        content = ctx.message.content
        channel = app.app.get_channel(935887688085680128)
        process = content.replace("!say", "").strip()
        await channel.send(process)



def setup(app):
    app.add_cog(Utility(app))
