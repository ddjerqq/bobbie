import asyncio as aio
import disnake
from disnake.ext import commands
from client.client import Client
from database.factories.user_factory import UserFactory


class OnReady(commands.Cog):
    def __init__(self, client: Client):
        self.client = client
        self.all_ids: set[int] = set()

    async def add_or_update_new_users_in_a_guild(self, guild: disnake.Guild):
        for member in filter(lambda u: not u.bot, guild.members):
            if member.id not in self.all_ids:
                user = UserFactory.new(member.id, member.name)
                await self.client.db.users.add(user)
                await self.client.logger.log(f"added {user}")

    async def add_or_update_new_users(self):
        group = [self.add_or_update_new_users_in_a_guild(guild) for guild in self.client.guilds]
        await aio.gather(*group)

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.logger.log(f"logged in as {self.client.user}")
        all_users = await self.client.db.users.get_all()
        self.all_ids = set(map(lambda u: u.id, all_users))
        await self.add_or_update_new_users()


def setup(client: Client):
    client.add_cog(OnReady(client))
