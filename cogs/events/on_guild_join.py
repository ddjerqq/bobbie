import disnake
from disnake.ext import commands
from client.client import Client
from database.factories.user_factory import UserFactory


class OnGuildJoin(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    @commands.Cog.listener()
    async def on_guild_join(self, guild: disnake.Guild):
        await self.client.logger.log(f"joined ({guild.id}) {guild.name}")

        for member in guild.members:
            if member.bot:
                continue

            user = UserFactory.new(member.id, member.name)
            await self.client.db.users.add(user)
            await self.client.logger.log(f"added {member.id}")


def setup(client: Client):
    client.add_cog(OnGuildJoin(client))
