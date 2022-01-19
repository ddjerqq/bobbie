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


app = App(intents=intents)
app.run("OTMzMjQzODQwOTA1NzY5MDQw.YeetDg.--AR1OpWo1NZkLz-jzC0PaOuJmI")
