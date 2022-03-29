import discord
import os
from discord.ext import commands


intents = discord.Intents.default()
intents.members = True
app = commands.Bot(command_prefix="!", help_command=None, intents=intents, case_insensitive=True)


@app.command()
async def load(ctx, extension):
    app.load_extension(f"cogs{extension}")


@app.command
async def unload(ctx, extension):
    app.unload_extension(f"cogs{extension}")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        app.load_extension(f"cogs.{filename[:-3]}")


app.run("OTU4MTA3OTA1NzkyNTQ0ODA5.YkIhhQ.YduxqTYY1SVVhQ84C_Ev_WBVC1M")
