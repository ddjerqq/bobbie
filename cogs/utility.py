import discord
import json
import requests as r
from discord.ext import commands

import app


class Utility(commands.Cog):

    def __init__(self, app):
        self.app = app

    @commands.command()
    async def avatar(self, ctx, avamember: discord.Member = None):
        try:
            if avamember is None:
                avamember = ctx.message.author
                print(avamember)
                await ctx.send(avamember.avatar_url)
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
