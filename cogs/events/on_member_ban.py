import disnake
from disnake.ext import commands
from client.client import Client


class OnMemberBan(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    @commands.Cog.listener()
    async def on_member_ban(self, guild: disnake.Guild, member: disnake.Member):
        user = await self.client.db.users.get(member.id)
        await self.client.db.users.delete(user.id)
        if user and user.marriage_id:
            # await self.client.db.marriages.delete(user.marriage_id)
            bride_role = guild.get_role(user.marriage_id.bride_role_id)
            king_role = guild.get_role(user.marriage_id.king_role_id)
            if bride_role:
                await bride_role.delete(reason="Banned")
            if king_role:
                await king_role.delete(reason="Banned")

        await self.client.logger.log(f"{member.name}#{member.discriminator} id=({member.id}) got banned in {guild.name}")


def setup(client: Client):
    client.add_cog(OnMemberBan(client))
