import base64
import random
from hashlib import md5

import disnake
from disnake.ext import commands
from client.client import Client


class OnMessage(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    @staticmethod
    def generate_confession_id(author_id: int) -> str:
        """
        to retrieve do:
        >>> confession_id = confession_id[::-1].swapcase()
        >>> id_ = base64.b64decode(confession_id.encode())
        >>> id_ = int(id_)
        >>> id_ >>= 16
        >>> id_ -= 0xB00B5_B00B5_B00B5
        >>> return id
        """
        id = author_id + 0xB00B5_B00B5_B00B5
        id <<= 16
        id += random.randint(0, 0xFFFF)
        id = str(id)
        encoding = base64.b64encode(id.encode()).decode()
        return encoding[::-1].swapcase()

    # Confessions
    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.channel.id in self.client.config["channels"]["confessions"]:
            if message.author != self.client.user:
                await message.delete()
                color = random.randint(0, 0xFFFFFF)
                id_   = self.generate_confession_id(message.author.id)
                em = disnake.Embed(
                    color=color,
                    description=message.content,
                )
                em.set_footer(text=f"ID: {id_}")
                await message.channel.send(embed=em)


def setup(client: Client):
    client.add_cog(OnMessage(client))
