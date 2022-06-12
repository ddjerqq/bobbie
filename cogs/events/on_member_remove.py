import disnake
from disnake.ext import commands
from client import Client


class OnMemberRemove(commands.Cog):
    def __init__(self, client: Client):
        self.client = client
        self.leave_channel: None | disnake.TextChannel = None

    @commands.Cog.listener()
    async def on_ready(self):
        self.leave_channel = self.client.get_channel(
            self.client.LEAVE_CHANNEL_ID
        )

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        em = await self.client.embeds.member_leave(member)
        await self.leave_channel.send(embed=em)
        # move to client ^^^^^^^


def setup(client: Client):
    client.add_cog(OnMemberRemove(client))
