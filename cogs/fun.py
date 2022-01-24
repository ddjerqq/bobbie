import discord
import json
import requests as r
from random import randint
from discord.ext import commands


class Commands(commands.Cog, commands.Bot):

    def __init(self, app):
        self.app = app

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def gay(self, ctx):
        content = ctx.message.content
        process = str(content).replace("!gay", "").strip()
        embed = discord.Embed(title="გეი ჰორმონების პროცენტის გამოცნობის მექანიზმი", color=0x2d56a9)
        random = randint(1, 100)
        embed.add_field(name="ტესტის რეზულტატი".format(ctx.message.author.mention),
                        value="{0}'მ გატესტა მექანიზმი და აღმოაჩინა რომ {1} {2} პროცენტით გეია 🏳️‍🌈.".format(
                            ctx.message.author.mention, process, random), inline=False)
        if not process:
            await ctx.send("ვინმე დაპინგე!")
        else:
            await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def coffee(self, ctx):
        content = ctx.message.content
        process = str(content).replace("!coffee", "").strip()
        if not process:
            await ctx.send("ვინმე დაპინგე!")
        else:
            await ctx.send("%s დაპატიჟა ყავაზე %s ☕" % (ctx.message.author.mention, process))
        await ctx.message.delete()

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def tea(self, ctx):
        content = ctx.message.content
        process = str(content).replace("!tea", "").strip()
        if not process:
            await ctx.send("ვინმე დაპინგე!")
        else:
            await ctx.send("%s შესთავაზა ჩაი %s ☕" % (ctx.message.author.mention, process))
        await ctx.message.delete()

    @commands.command()
    @commands.cooldown(1, 30, commands.BucketType.user)
    async def hug(self, ctx):
        content = ctx.message.content
        process = str(content).replace("!hug", "").strip()
        if not process:
            await ctx.send("ვინმე დაპინგე!")
        else:
            await ctx.send("%s გულიანად ჩაეხუტა %s'ს🫂" % (ctx.message.author.mention, process))
        await ctx.message.delete()


def setup(app):
    app.add_cog(Commands(app))