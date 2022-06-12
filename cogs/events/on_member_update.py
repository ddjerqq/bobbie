import disnake
from disnake.ext import commands
from client import Client


class OnMemberUpdate(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_update(self, before: disnake.Member, after: disnake.Member):
        """TO ADD"""


def setup(client: Client):
    client.add_cog(OnMemberUpdate(client))
