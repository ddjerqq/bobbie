import disnake
from disnake.ext import commands
from client.client import Client
from database.factories.user_factory import UserFactory
from database.models.user import User


class OnMemberRemove(commands.Cog):
    def __init__(self, client: Client):
        self.client = client
        self.leave_channels = []  # type: list[disnake.TextChannel]


    @commands.Cog.listener()
    async def on_ready(self):
        self.leave_channels = [self.client.get_channel(id_) for id_ in self.client.config["channels"]["leave"]
                               if self.client.get_channel(id_)]


    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        em = await self.client.embeds.utils.member_leave(member)
        for channel in self.leave_channels:
            await channel.send(embed=em)


    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        if member.bot:
            return
        old_user = await self.client.db.users.get(member.id)
        if old_user is None:
            user = UserFactory.new(member.id, member.name)
            await self.client.db.users.add(user)
            await self.client.logger.log(f"added {user}")


    @commands.Cog.listener()
    async def on_member_ban(self, guild: disnake.Guild, member: disnake.Member):
        await self.client.logger.log(
            f"{member.name}#{member.discriminator} id=({member.id}) got banned in {guild.name}")

        user = await self.client.db.users.get(member.id)
        if not user:
            return

        if user.marriage_id:
            marriage = await self.client.db.marriages.get(user.marriage_id)
            if marriage.guild_id != guild.id:
                return

            bride_role = guild.get_role(marriage.bride_role_id)
            king_role  = guild.get_role(marriage.king_role_id)

            if bride_role:
                await bride_role.delete(reason="Banned")
            if king_role:
                await king_role.delete(reason="Banned")

            bride_id = marriage.bride_id if user.id == marriage.king_id else marriage.king_id
            bride = await self.client.db.users.get(bride_id)
            bride.marriage_id = None
            user.marriage_id  = None

            await self.client.db.users.update(user)
            await self.client.db.users.update(bride)
            await self.client.db.marriages.delete(marriage.id)


    @commands.Cog.listener()
    async def on_user_update(self, before: disnake.User, after: disnake.User):
        if before.bot:
            return
        if before.name != after.name:
            user = await self.client.db.users.get(after.id)
            if isinstance(user, User):
                user.name = after.name
                await self.client.db.users.update(user)
            else:
                user = UserFactory.new(after.id, after.name)
                await self.client.db.users.add(user)


def setup(client: Client):
    client.add_cog(OnMemberRemove(client))
