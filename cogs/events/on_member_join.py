import disnake
from disnake.ext import commands
from client.client import Client
from database.factories.user_factory import UserFactory


class OnMemberJoin(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        user = UserFactory.new(member.id, member.name)
        await self.client.db.users.add(user)
        await self.client.logger.log(f"added ({member.id}) {member.name}")


def setup(client: Client):
    client.add_cog(OnMemberJoin(client))
