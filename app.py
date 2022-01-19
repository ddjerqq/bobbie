import discord
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
            process_message = str(content).replace("!say", "").strip()
            channel = app.get_channel(740486454240870420)
            await channel.send(process_message)



app = App(intents=intents)
app.run("OTMzMjQzODQwOTA1NzY5MDQw.YeetDg.--AR1OpWo1NZkLz-jzC0PaOuJmI")
