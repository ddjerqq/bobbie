import disnake
from disnake.ext import commands
from client import Client


class OnMemberBan(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_ban(self, guild: disnake.Guild, user: disnake.Member):
        await self.client.log(f"{user.name}#{user.discriminator} id=({user.id}) got banned in {guild.name}")
