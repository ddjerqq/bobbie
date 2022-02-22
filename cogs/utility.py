import discord
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
                embed = discord.Embed(color=0x2d56a9)
                embed.add_field(name="%s" % avamember, value="ID: %s" % avamember.id, inline=True)
                embed.set_image(url=avamember.avatar_url)
                await ctx.send(embed=embed)
            else:
                embed = discord.Embed(color=0x2d56a9)
                embed.add_field(name="%s" % avamember, value="ID: %s" % avamember.id, inline=True)
                embed.set_image(url=avamember.avatar_url)
                await ctx.send(embed=embed)
        except AttributeError as e:
            await ctx.send(e)

    @commands.command()
    async def say(self, ctx):
        content = ctx.message.content
        channel = app.app.get_channel(935887688085680128)
        process = content.replace("!say", "").strip()
        await channel.send(process)

    @commands.command()
    async def userinfo(self, ctx, target: discord.Member = None):
        try:
            if target is None:
                target = ctx.message.author
                embed = discord.Embed(color=0x2d56a9)
                embed.add_field(name="%s" % target, value="ID: %s" % target.id, inline=False)
                embed.add_field(name="დაჯოინდა", value="%s-%s-%s" % (target.joined_at.day, target.joined_at.month, target.joined_at.year), inline=True)
                embed.add_field(name="რეგისტრაცია", value="%s-%s-%s" % (target.created_at.day, target.created_at.month, target.created_at.year), inline=True)
                embed.set_thumbnail(url=target.avatar_url)
                await ctx.send(embed=embed)
            else:
                roles = "".join(target.roles)
                embed = discord.Embed(color=0x2d56a9)
                embed.add_field(name="%s" % target.name, value="ID: %s" % target.name, inline=False)
                embed.add_field(name="დაჯოინდა", value="%s-%s-%s" % (target.joined_at.day, target.joined_at.month, target.joined_at.year), inline=True)
                embed.add_field(name="რეგისტრაცია", value="%s-%s-%s" % (target.created_at.day, target.created_at.month, target.created_at.year), inline=True)
                embed.set_thumbnail(url=target.avatar_url)
                await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(e)


def setup(app):
    app.add_cog(Utility(app))
