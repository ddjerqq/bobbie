import disnake
from disnake.ext import commands
from client.client import Client


class OnMessageDelete(commands.Cog):
    def __init__(self, client: Client):
        self.client = client
        self.deleted_messages_channels = []  # type: None | list[disnake.TextChannel]

    def message_delete_check(self, message: disnake.Message) -> bool:
        filtered_channels = self.client.config["channels"]["deleted_msgs"] + \
                            self.client.config["channels"]["confessions"]

        if message.guild.id == 935886444109631510:
            if not message.author.bot:
                if message.author != self.client.user:
                    if message.channel.id not in filtered_channels:
                        return True
        return False

    @commands.Cog.listener()
    async def on_ready(self):
        for id_ in self.client.config["channels"]["deleted_msgs"]:
            channel = self.client.get_channel(id_)
            if channel:
                self.deleted_messages_channels.append(channel)

    @commands.Cog.listener()
    async def on_message_delete(self, message: disnake.Message):
        if self.message_delete_check(message):
            em = self.client.embeds.utils.deleted_message(message)
            for channel in self.deleted_messages_channels:
                await channel.send(embed=em)


def setup(client):
    client.add_cog(OnMessageDelete(client))
