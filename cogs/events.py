import disnake
from utils import *
from disnake.ext import commands
from client import Client
from database.models.user import User


class Events(commands.Cog):
    def __init__(self, client: Client):
        self.client = client
        self.confession_channel: disnake.TextChannel | None = None
        self.deleted_messages_channel: disnake.TextChannel | None = None
        self.leave_channel: disnake.TextChannel | None = None


    async def add_or_update_new_users(self):
        for guild in self.client.guilds:
            for member in guild.members:
                if member.bot: continue

                user = await self.client.db.users.get(member.id)

                if not isinstance(user, User):
                    await self.client.db.users.add(member.id, member.name)
                    await self.client.log(f"added ({member.id}) {member.name}")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.log("bobbi online")

        self.confession_channel       = self.client.get_channel(CONFESSION_CHANNEL_ID)
        self.deleted_messages_channel = self.client.get_channel(DELETE_MESSAGE_LOG)
        self.client.log_channel       = self.client.get_channel(LOG_CHANNEL_ID)
        self.leave_channel            = self.client.get_channel(LEAVE_CHANNEL_ID)

        await self.add_or_update_new_users()

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.channel.id == CONFESSION_CHANNEL_ID:
            await message.delete()
            embed = disnake.Embed(color=0x2d56a9, description=message.content)
            await message.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        await self.client.db.users.add(member.id, member.name)
        await self.client.log(f"added ({member.id}) {member.name}")

    @commands.Cog.listener()
    async def on_message_delete(self, message: disnake.Message):
        whitelist = ["!gay", "!coffee", "!tea", "!hug", "!beer", "?ban", "?kick", "?purge", "?mute", "?unmute",
                     "!slap", "!popcorn"]

        if message.author == self.client.user: return
        if message.channel.id == CONFESSION_CHANNEL_ID: return
        if message.channel.id == DELETE_MESSAGE_LOG: return
        if any(message.content.startswith(w) for w in whitelist): return

        em = self.client.embeds.message_delete(message)
        await self.deleted_messages_channel.send(embed=em)

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        em = await self.client.embeds.member_leave(member)
        await self.leave_channel.send(embed=em)


def setup(client):
    client.add_cog(Events(client))
