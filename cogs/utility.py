import discord
import json
import requests as r
from discord.ext import commands


class Utility(commands.Cog):

    def __init__(self, app):
        self.app = app

    @commands.command()
    async def weather(self, ctx, arg):
        key = "10d195e2163c3b8d5b62bfeec7f45da0"
        data = r.get("https://api.openweathermap.org/data/2.5/weather?q=%s&appid=67693c9353acbcb58d6ace5e51825990/" % arg)
        with open("cogs/weather.json", "w+") as f:
            json.dump(data.json(), f, indent=4)


    @commands.command()
    async def avatar(self, ctx, *, avamember: discord.Member = None):
        avatar = avamember.avatar_url
        try:
            await ctx.send(avatar)
        except AttributeError as e:
            await ctx.send(e)


def setup(app):
    app.add_cog(Utility(app))
