import discord
import json

import requests as r

intents = discord.Intents.default()
intents.members = True

class App(discord.Client):
    async def on_ready(self):
        print("Connected:", self.user)

app = App(intents=intents)
app.run(token="OTMzMjQzODQwOTA1NzY5MDQw.YeetDg.--AR1OpWo1NZkLz-jzC0PaOuJmI")