import discord
import random
import os
import json
from discord.ext import commands

import requests as r

intents = discord.Intents.default()
intents.members = True
app = commands.Bot(command_prefix="!")


@app.command()
async def load(ctx, extension):
    app.load_extension(f"cogs{extension}")


@app.command
async def unload(ctx, extension):
    app.unload_extension(f"cogs{extension}")


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        app.load_extension(f"cogs.{filename[:-3]}")


class App(discord.Client):
    async def on_ready(self):
        print("Connected:", self.user)
        try:
            game = discord.Game("discord.gg/georgia")
            status = discord.Status.dnd
            await app.change_presence(status=status, activity=game)
        except Exception as e:
            print("Something went wrong:", e)
            exit()

    """async def on_message(self, message):
        if message.content.startswith("!say"):
            content = message.content
            process_message = str(content).replace("!say", "").strip()
            channel = app.get_channel(740486454240870420)
            if message.author.id != 834942471808483349:
                await message.channel.send("რაებს ჩალიჩობ ბრატ?")
            else:
                await channel.send(process_message)

        if message.content.startswith("!gay"):
            content = message.content
            process = str(content).replace("!gay", "").strip()
            random_number = random.randint(1, 100)
            number = str(random_number)
            if not process:
                await message.channel.send("ვინმე დაპინგე!")
            else:
                await message.channel.send("%s %s პროცენტით გეია. 🏳️‍🌈" % (process, number))

        if message.content.startswith("!tea"):
            content = message.content
            process = str(content).replace("!tea", "").strip()
            if not process:
                await message.channel.send("ვინმე დაპინგე!")
            else:
                await message.channel.send("%s'მ შესთავაზა ჩაი %s'ს. ☕" % (message.author.mention, process))

        if message.content.startswith("!coffee"):
            content = message.content
            process = str(content).replace("!coffee", "").strip()
            if not process:
                await message.channel.send("ვინმე დაპინგე!")
            else:
                await message.channel.send("%s'მ მოიწვია ყავაზე %s. ☕" % (message.author.mention, process))"""


# app = App(intents=intents)
app.run("OTMzMjQzODQwOTA1NzY5MDQw.YeetDg.--AR1OpWo1NZkLz-jzC0PaOuJmI")
