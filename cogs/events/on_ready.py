import disnake
from disnake.ext import commands
from client import Client
from database.factories.user_factory import UserFactory
from database.models.user import User


class OnReady(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    async def add_or_update_new_users(self):
        all_users = await self.client.db.users.get_all()
        all_ids = list(map(lambda u: u.id, all_users))

        for guild in self.client.guilds:
            for member in filter(lambda m: not m.bot, guild.members):
                if member.id not in all_ids:
                    user = UserFactory.new(member.id, member.name)
                    await self.client.db.users.add(user)
                    await self.client.log(f"added ({member.id}) {member.name}")


    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.log("bobbi online")
