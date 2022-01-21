import discord
from random import randint
from discord.ext import commands


class Commands(commands.Cog):

    def __init(self, app):
        self.app = app

    @commands.command()
    async def gay(self, ctx):
        content = ctx.message.content
        process = str(content).replace("!gay", "").strip()
        if not process:
            await ctx.send("ვინმე დაპინგე!")
        else:
            await ctx.send("%s %s პროცენტით გეია 🏳️‍🌈" % (process, randint(1, 100)))

    @commands.command()
    async def coffee(self, ctx):
        content = ctx.message.content
        process = str(content).replace("!coffee", "").strip()
        if not process:
            await ctx.send("ვინმე დაპინგე!")
        else:
            await ctx.send("%s დაპატიჟა ყავაზე %s ☕" % (ctx.message.author.mention, process))

    @commands.command()
    async def tea(self, ctx):
        content = ctx.message.content
        process = str(content).replace("!tea", "").strip()
        if not process:
            await ctx.send("ვინმე დაპინგე!")
        else:
            await ctx.send("%s შესთავაზა ჩაი %s ☕" % (ctx.message.author.mention, process))


def setup(app):
    app.add_cog(Commands(app))
