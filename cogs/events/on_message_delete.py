import disnake
from disnake.ext import commands
from client.client import Client


class OnMessageDelete(commands.Cog):
    def __init__(self, client: Client):
        self.client = client
        self.deleted_messages_channel = None  # type: None | disnake.TextChannel

    def message_check(self, message: disnake.Message) -> bool:
        if message.guild.id == 935886444109631510:
            if message.author != self.client.user:
                if message.channel.id != self.client.DELETE_MESSAGE_LOG:
                    return True
        return False

    @commands.Cog.listener()
    async def on_ready(self):
        self.deleted_messages_channel = self.client.get_channel(
            self.client.DELETE_MESSAGE_LOG
        )

    @commands.Cog.listener()
    async def on_message_delete(self, message: disnake.Message):
        if self.message_check(message):
            em = self.client.embeds.message_delete(message)
            await self.deleted_messages_channel.send(embed=em)


def setup(client):
    client.add_cog(OnMessageDelete(client))
