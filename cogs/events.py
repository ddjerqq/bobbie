import random
import disnake
from utils import *
from disnake.ext import commands
from models.client import Client


class Events(commands.Cog):
    def __init__(self, client: Client):
        self.client = client
        self.confession_channel: disnake.TextChannel | None = None
        self.deleted_messages_channel: disnake.TextChannel | None = None


    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.log("bobbi online")

        self.confession_channel       = self.client.get_channel(CONFESSION_CHANNEL_ID)
        self.deleted_messages_channel = self.client.get_channel(DELETE_MESSAGE_LOG)
        self.client.log_channel       = self.client.get_channel(LOG_CHANNEL_ID)

        for guild in self.client.guilds:
            for member in guild.members:
                if member.bot: continue

                user = await self.client.db.user_service.get(member.id)

                if user is None:
                    await self.client.db.user_service.add(member.id, member.name)
                    await self.client.log(f"added ({member.id}) {member.name}")


    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        if message.author == self.client.user: return

        user = await self.client.db.user_service.get(message.author.id)
        if user is not None:
            user.experience += 1
            await self.client.db.user_service.update(user)

        if message.channel.id == CONFESSION_CHANNEL_ID:
            await message.delete()

            embed = disnake.Embed(color=0x2d56a9, description=message.content)
            id = random.randint(1_000_000_000, 9_999_999_999)
            embed.set_footer(text = f"confession ID: {id}")
            await self.client.log(f"confession with id: {id} was sent by: {user.username}:{user.id}")
            await message.channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        await self.client.db.user_service.add(member.id, member.name)
        await self.client.log(f"added ({member.id}) {member.name}")


    @commands.Cog.listener()
    async def on_message_delete(self, message: disnake.Message):
        whitelist = ["!gay", "!coffee", "!tea", "!hug", "!beer", "?ban", "?kick", "?purge", "?mute", "?unmute",
                     "!slap", "!popcorn"]

        if message.author == self.client.user: return
        if message.channel.id == CONFESSION_CHANNEL_ID: return
        if message.channel.id == DELETE_MESSAGE_LOG: return
        if any(message.content.startswith(w) for w in whitelist): return

        embed = disnake.Embed(title=f"{message.author.name}\nID: {message.author.id}",
                              color=0x2d56a9,
                              timestamp=disnake.utils.utcnow())
        embed.set_thumbnail(url=message.author.avatar.url)
        embed.add_field(name="ჩანელი", value=message.channel.mention, inline=False)


        if message.attachments:
            embed.add_field(
                name="ათაჩმენტ(ებ)ი",
                value="\n".join(map(lambda a: a.url, message.attachments)))

        if message.content:
            embed.add_field(
                name="მესიჯი",
                value=message.content, inline=False)

        await self.deleted_messages_channel.send(embed=embed)


def setup(client):
    client.add_cog(Events(client))
