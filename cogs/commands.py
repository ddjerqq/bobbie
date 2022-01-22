import discord
import json
import requests as r
from random import randint
from discord.ext import commands


class Commands(commands.Cog, commands.Bot):

    def __init(self, app):
        self.app = app

    @commands.command()
    async def gay(self, ctx):
        content = ctx.message.content
        process = str(content).replace("!gay", "").strip()
        if not process:
            await ctx.send("ვინმე დაპინგე!")
        elif "denis" in process:
            await ctx.send("%s 100 პროცენტით გეია" % process)
        else:
            await ctx.send("%s %s პროცენტით გეია 🏳️‍🌈" % (process, randint(1, 100)))
        await ctx.message.delete()

    @commands.command()
    async def coffee(self, ctx):
        content = ctx.message.content
        process = str(content).replace("!coffee", "").strip()
        if not process:
            await ctx.send("ვინმე დაპინგე!")
        else:
            await ctx.send("%s დაპატიჟა ყავაზე %s ☕" % (ctx.message.author.mention, process))
        await ctx.message.delete()

    @commands.command()
    async def tea(self, ctx):
        content = ctx.message.content
        process = str(content).replace("!tea", "").strip()
        if not process:
            await ctx.send("ვინმე დაპინგე!")
        else:
            await ctx.send("%s შესთავაზა ჩაი %s ☕" % (ctx.message.author.mention, process))
        await ctx.message.delete()

    @commands.command()
    async def hug(self, ctx):
        content = ctx.message.content
        process = str(content).replace("!hug", "").strip()
        if not process:
            await ctx.send("ვინმე დაპინგე!")
        else:
            await ctx.send("%s გულიანად ჩაეხუტა %s 🫂'ს" % (ctx.message.author.mention, process))
        await ctx.message.delete()

    @commands.command()
    async def weather(self, ctx, arg):
        geolocate = Nominatim(user_agent="Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) "
                                         "Chrome/41.0.2228.0 Safari/537.36")
        weather_api = "https://api.darksky.net/forecast/abe6a84811a8ab8f1f39cd9b8b8f40e1/{},{}"
        location = geolocate.geocode(arg)
        process = r.get(weather_api.format(location.latitude, location.longitude))
        with open("cogs/weather.json", "w") as w:
            json.dump(process.json(), w, indent=4)
        with open("cogs/weather.json", "r+") as weather:
            weather_data = json.load(weather)
        await ctx.send("weather in %s: %s" % (arg, weather_data["currently"]["summary"]))


def setup(app):
    app.add_cog(Commands(app))
