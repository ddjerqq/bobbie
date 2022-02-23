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
                embed.add_field(name="დაჯოინდა", value="%s-%s-%s" % (
                target.joined_at.day, target.joined_at.month, target.joined_at.year), inline=True)
                embed.add_field(name="რეგისტრაცია", value="%s-%s-%s" % (
                target.created_at.day, target.created_at.month, target.created_at.year), inline=True)
                embed.set_thumbnail(url=target.avatar_url)
                await ctx.send(embed=embed)
            else:
                roles = "".join(target.roles)
                embed = discord.Embed(color=0x2d56a9)
                embed.add_field(name="%s" % target.name, value="ID: %s" % target.name, inline=False)
                embed.add_field(name="დაჯოინდა", value="%s-%s-%s" % (
                target.joined_at.day, target.joined_at.month, target.joined_at.year), inline=True)
                embed.add_field(name="რეგისტრაცია", value="%s-%s-%s" % (
                target.created_at.day, target.created_at.month, target.created_at.year), inline=True)
                embed.set_thumbnail(url=target.avatar_url)
                await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(e)


@commands.Cog.listener()
async def on_message_delete(message):
    channel = app.get_channel(939534645798793247)
    msg_content = message.content
    msg_author = message.author
    author_id = message.author.id
    embed = discord.Embed(title="Bobbie's Archives", description="ბობიმ შეამჩნია წაშლილი მესიჯი მაგრამ მოასწრო "
                                                                 "სქრინის გადაღება!", color=0x2d56a9)
    embed.add_field(name="ავტორი", value="%s" % msg_author, inline=True)
    embed.add_field(name="ID", value="%s" % author_id, inline=True)
    embed.add_field(name="მესიჯი", value="%s" % msg_content, inline=False)
    words = ["!gay", "!coffee", "!tea", "!hug", "!beer", "?ban", "?kick", "?purge", "?mute", "?unmute"]
    if any(word in msg_content for word in words):
        pass
    elif msg_author == 933243840905769040:
        pass
    else:
        await channel.send(embed=embed)


@commands.Cog.listener()
async def on_member_remove(member):
    member_name = member.name
    member_id = member.id
    channel = app.get_channel(942800528822370315)
    embed = discord.Embed(color=0x2d56a9)
    embed.add_field(name="სახელი", value="%s" % member_name, inline=True)
    embed.add_field(name="ID", value="%s" % member_id, inline=True)
    embed.set_thumbnail(url=member.avatar_url)
    await channel.send(embed=embed)


@commands.Cog.listener()
async def on_message_edit(message_before, message_after):
    if message_before.channel.id == 936740832105603173:
        embed = discord.Embed(description="ვიღაცამ დაარედაქტირა მესიჯი, შესაძლოა თამაშის გაფუჭებას ცდილობს! ყურადღებით "
                                          "წაიკითხე დაბლა!", color=0x2d56a9)
        embed.add_field(name="დარედაქტირებული მესიჯი", value="%s" % message_after.content, inline=False)
        embed.add_field(name="ორიგინალური მესიჯი", value="%s" % message_before.content, inline=True)
        embed.set_footer(text="დაარედაქტირა: %s" % message_before.author, icon_url=message_before.author.avatar_url)
        await message_before.channel.send(embed=embed)
    else:
        pass


def setup(app):
    app.add_cog(Utility(app))
