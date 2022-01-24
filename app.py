import discord
import random
import os
import json
from discord.ext import commands

import requests as r

intents = discord.Intents.default()
intents.members = True
app = commands.Bot(command_prefix="!", help_command=None)


@app.command()
async def load(ctx, extension):
    app.load_extension(f"cogs{extension}")


@app.command
async def unload(ctx, extension):
    app.unload_extension(f"cogs{extension}")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        app.load_extension(f"cogs.{filename[:-3]}")


@app.listen("on_message")
async def neko(message):
    emoji = app.get_emoji(935132922669842452)
    if message.content.startswith("neko" or "Neko"):
        await message.channel.send("https://cdn.discordapp.com/emojis/451544987952218112.gif?size=96&quality=lossless")


app.run("OTMzMjQzODQwOTA1NzY5MDQw.YeetDg.b4icjZ7hgbXTtTn_4GR-QWYKyuw")
