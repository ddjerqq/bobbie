import discord
import random
import json

import requests as r

intents = discord.Intents.default()
intents.members = True


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

    async def on_message(self, message):
        if message.content.startswith("!say"):
            content = message.content
            author = message.author.id
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
                await message.channel.send("%s %s პროცენტით გეია." % (process, number))



app = App(intents=intents)
app.run("OTMzMjQzODQwOTA1NzY5MDQw.YeetDg.--AR1OpWo1NZkLz-jzC0PaOuJmI")
