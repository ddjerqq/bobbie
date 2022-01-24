import discord
from discord.ext import commands


class Utility(commands.Cog):

    def __init__(self, app):
        self.app = app

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

    @commands.command()
    async def avatar(self, ctx, *, avamember: discord.Member = None):
        avatar = avamember.avatar_url
        try:
            await ctx.send(avatar)
        except AttributeError as e:
            await ctx.send(e)


def setup(app):
    app.add_cog(Utility(app))
