from disnake.ext import commands
from client.client import Client


class ModerationCommands(commands.Cog):
    def __init__(self, client: Client):
        self.client = client


def setup(client):
    client.add_cog(ModerationCommands(client))
