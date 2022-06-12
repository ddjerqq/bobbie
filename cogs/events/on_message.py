import random

import disnake
from disnake.ext import commands
from client.client import Client


class OnMessage(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.channel.id in self.client.CONFESSION_CHANNELS:
            if message.author != self.client.user:
                await message.delete()
                color = random.randint(0, 16777215)
                embed = disnake.Embed(color=color, description=message.content)
                await message.channel.send(embed=embed)

        await self.client.process_commands(message)


def setup(client: Client):
    client.add_cog(OnMessage(client))
