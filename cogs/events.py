import random

import disnake
from disnake.ext import commands
from client import Client
from database.models.user import User


class Events(commands.Cog):
    def __init__(self, client: Client):
        self.client = client
        self.confession_channels      = None  # type: None | list[disnake.TextChannel]
        self.deleted_messages_channel = None  # type: None | disnake.TextChannel
        self.leave_channel            = None  # type: None | disnake.TextChannel


    async def add_or_update_new_users(self):
        for guild in self.client.guilds:
            for member in guild.members:
                if member.bot: continue

                user = await self.client.db.users.get(member.id)

                if not isinstance(user, User):
                    user = User.new(member.id, member.name)
                    await self.client.db.users.add(user)
                    await self.client.log(f"added ({member.id}) {member.name}")

    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.log("bobbi online")

        self.confession_channels      = [self.client.get_channel(id) for id in self.client.CONFESSION_CHANNELS]
        self.deleted_messages_channel = self.client.get_channel(self.client.DELETE_MESSAGE_LOG)
        self.client.log_channel       = self.client.get_channel(self.client.LOG_CHANNEL_ID)
        self.leave_channel            = self.client.get_channel(self.client.LEAVE_CHANNEL_ID)

        await self.add_or_update_new_users()

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.channel.id in self.client.CONFESSION_CHANNELS and message.author != self.client.user:
            await message.delete()
            color = random.randint(0, 16777215)
            embed = disnake.Embed(color=color, description=message.content)
            await message.channel.send(embed=embed)

        await self.client.process_commands(message)

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        user = User.new(member.id, member.name)
        await self.client.db.users.add(user)
        await self.client.log(f"added ({member.id}) {member.name}")

    def message_check(self, message: disnake.Message) -> bool:
        return \
            message.author != self.client.user \
            and message.channel.id != self.client.DELETE_MESSAGE_LOG \
            and message.guild.id == 935886444109631510

    @commands.Cog.listener()
    async def on_message_delete(self, message: disnake.Message):
        if self.message_check(message):
            em = self.client.embeds.message_delete(message)
            try:
                await self.deleted_messages_channel.send(embed=em)
            except AttributeError:
                pass

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        em = await self.client.embeds.member_leave(member)
        await self.leave_channel.send(embed=em)

    @commands.Cog.listener()
    async def on_guild_join(self, guild: disnake.Guild):
        await self.client.log(f"joined {guild.name}")

        for member in guild.members:
            if member.bot:
                continue
            user = User.new(member.id, member.name)
            await self.client.db.users.add(user)
            await self.client.log(f"added ({member.id}) {member.name}")


def setup(client):
    client.add_cog(Events(client))
