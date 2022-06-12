import disnake
from disnake.ext import commands
from client import Client
from database.factories.user_factory import UserFactory
from database.models.user import User


class OnUserUpdate(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    @commands.Cog.listener()
    async def on_user_update(self, before: disnake.User, after: disnake.User):
        if before.name != after.name:
            user = await self.client.db.users.get(after.id)
            if isinstance(user, User):
                user.name = after.name
                await self.client.db.users.update(user)
            else:
                user = UserFactory.new(after.id, after.name)
                await self.client.db.users.add(user)


def setup(client: Client):
    client.add_cog(OnUserUpdate(client))
