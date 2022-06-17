import disnake
from disnake.ext import commands
from client.client import Client


class OnMemberUpdate(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_update(self, before: disnake.Member, after: disnake.Member):
        """timeout members who play league more than 1hr for 1 day"""
        # TODO
        # for activity in after.activities:
        #     if isinstance(activity, disnake.Game):
        #         activity  # type: disnake.Game
        #         print(activity.name == League of Legends)
        #         print(activity.type)
        #         print(activity.created_at)
        #         print(activity.start)
        #         print(activity)


def setup(client: Client):
    client.add_cog(OnMemberUpdate(client))
