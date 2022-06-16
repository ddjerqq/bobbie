import disnake
from disnake.ext import commands
from client.client import Client


class OnMemberRemove(commands.Cog):
    def __init__(self, client: Client):
        self.client = client
        self.leave_channels = []  # type: list[disnake.TextChannel]

    @commands.Cog.listener()
    async def on_ready(self):
        for id_ in self.client.config["channels"]["leave"]:
            channel = self.client.get_channel(id_)
            if channel:
                self.leave_channels.append(channel)

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        em = await self.client.embeds.utils.member_leave(member)
        for channel in self.leave_channels:
            await channel.send(embed=em)


def setup(client: Client):
    client.add_cog(OnMemberRemove(client))
