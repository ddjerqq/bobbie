import discord
import os
from discord.ext import commands


intents = discord.Intents.default()
intents.members = True
app = commands.Bot(command_prefix="!", help_command=None, intents=intents)


@app.command()
async def load(ctx, extension):
    app.load_extension(f"cogs{extension}")


@app.command
async def unload(ctx, extension):
    app.unload_extension(f"cogs{extension}")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        app.load_extension(f"cogs.{filename[:-3]}")


@app.listen()
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
    words = ["!gay", "!coffee", "!tea", "!hug", "!beer", "?ban", "kick", "?purge"]
    if any(word in msg_content for word in words):
        pass
    elif msg_author == 933243840905769040:
        pass
    else:
        await channel.send(embed=embed)


@app.listen()
async def on_member_remove(member):
    member_name = member.name
    member_id = member.id
    channel = app.get_channel(942800528822370315)
    embed = discord.Embed()
    embed.add_field(name="სახელი", value="%s" % member_name, inline=True)
    embed.add_field(name="ID", value="%s" % member_id, inline=True)
    await channel.send(embed=embed)


app.run("OTMzMjQzODQwOTA1NzY5MDQw.YeetDg.0VU1hSrwSyGC96VVygS82L38zck")
