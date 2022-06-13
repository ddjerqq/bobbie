from disnake.ext import commands
from client.client import Client
from database.factories.user_factory import UserFactory


class OnReady(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    async def add_or_update_new_users(self):
        all_users = await self.client.db.users.get_all()
        all_ids   = list(map(lambda u: u.id, all_users))

        for guild in self.client.guilds:
            for member in guild.members:
                if member.bot:
                    continue
                if member.id not in all_ids:
                    user = UserFactory.new(member.id, member.name)
                    await self.client.db.users.add(user)
                    await self.client.logger.log(f"added {user}")


    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.logger.log("bobbi online")


def setup(client: Client):
    client.add_cog(OnReady(client))
