import random

import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction as Aci

from utils import *


class ApplicationCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.slash_command(name="gay", guild_ids=GUILD_IDS, description="გაიგე რამდენად გეია შენ ან სხვა")
    async def gay(self, inter: Aci, target: disnake.Member = None):
        target = target or inter.author

        embed = disnake.Embed(
            title="გეი ჰორმონების პროცენტის გამოცნობის მექანიზმი",
            color=0x2d56a9)

        howgay = random.randint(1, 100)

        embed.add_field(
            name="გეი ტესტის რეზულტატი",
            value=f"{inter.author.mention}'მ ჩაიტარა გეი გამოკვლების ტესტი და აღმოაჩინა რომ {target.mention} "
                  f"{howgay} პროცენთით გეია 🏳️‍🌈.")

        await inter.send(embed=embed)


    @commands.user_command(name="gay", guild_ids=GUILD_IDS)
    async def gay(self, inter: Aci, target: disnake.Member):
        embed = disnake.Embed(
            title = "გეი ჰორმონების პროცენტის გამოცნობის მექანიზმი",
            color = 0x2d56a9)

        embed.add_field(
            name = "გეი ტესტის რეზულტატი",
            value = f"{inter.author.mention}'მ ჩაიტარა გეი გამოკვლების ტესტი და აღმოაჩინა რომ {target.mention} "
                    f"{random.randint(1, 100)} პროცენთით გეია 🏳️‍🌈.")

        await inter.send(embed=embed)


    # @commands.command()
    # async def hug(self, ctx, target: disnake.Member = None):
    #     if target is None or target == ctx.message.author:
    #         await ctx.send("%s'მ მოიწყინა და დაუწყო თავის თავს მოფერება 🫂" % ctx.message.author.mention)
    #     else:
    #         await ctx.send("%s გულიანად ჩაეხუტა %s'ს🫂" % (ctx.message.author.mention, target.mention))
    #     await ctx.message.delete()
    #
    # @commands.command()
    # async def slap(self, ctx, target: disnake.Member = None):
    #     if target is None or target == ctx.message.author:
    #         await ctx.send("%s გააფრინა და თავის თავს გიჟივით დაუწყო ცემა ✊" % ctx.message.author.mention)
    #     else:
    #         await ctx.send("%s გაბრაზდა და ძლიერად შემოულაწუნა %s ✊" % (ctx.message.author.mention, target.mention))
    #     await ctx.message.delete()


def setup(client):
    client.add_cog(ApplicationCommands(client))
