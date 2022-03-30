import time
import random

import disnake
from disnake.ext import commands
from utils import *
from services import user_service
from models.database.database import database


class Events(commands.Cog):
    def __init__(self, client: disnake.Client):
        self.client = client
        self.confession_channel: disnake.TextChannel | None = None
        self.deleted_messages_channel: disnake.TextChannel | None = None


    @commands.Cog.listener()
    async def on_ready(self):
        log("bobbi online")

        self.confession_channel       = self.client.get_channel(CONFESSION_CHANNEL_ID)
        self.deleted_messages_channel = self.client.get_channel(MESSAGE_DELETE_LOG_CHANNEL_ID)

        for guild in self.client.guilds:
            for user in guild.members:
                if user.bot:
                    continue
                indb = await database.users.exists(user.id)
                if indb is None:
                    await user_service.add_user(user.id, user.name, user.joined_at)


    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        await user_service.give_exp(message.author.id, 1)

        if message.channel.id == CONFESSION_CHANNEL_ID and message.author != self.client.user:
            await message.delete()
            embed = confession_embed(message.content, message.author)
            await self.confession_channel.send(embed=embed)



    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        await user_service.add_user(member.id, member.name, member.joined_at)
        # greet user an rame maseti

    @commands.Cog.listener()
    async def on_message_delete(self, message: disnake.Message):
        whitelist = ["!gay", "!coffee", "!tea", "!hug", "!beer", "?ban", "?kick", "?purge", "?mute", "?unmute",
                     "!slap", "!popcorn"]

        if message.author == self.client.user:
            return

        if message.channel.id == CONFESSION_CHANNEL_ID:
            return

        if any(message.content.startswith(w) for w in whitelist):
            return

        embed = disnake.Embed(
            title=f"{message.author.name}\nID: {message.author.id}",
            color=0x2d56a9,
            timestamp=disnake.utils.utcnow()
        )

        embed.set_thumbnail(url=message.author.avatar.url)
        embed.add_field(name="ჩანელი", value=message.channel.mention, inline=False)

        if message.attachments:
            embed.add_field(
                name="ათაჩმენტ(ებ)ი",
                value="\n".join(map(lambda a: a.url, message.attachments)))

        if message.content:
            embed.add_field(name="მესიჯი", value=message.content, inline=False)

        await self.deleted_messages_channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        member_name = member.name
        member_id = member.id
        channel = self.client.get_channel(942800528822370315)
        embed = disnake.Embed(color=0x2d56a9)
        embed.add_field(name="სახელი", value="%s" % member_name)
        embed.add_field(name="ID", value="%s" % member_id)
        embed.set_thumbnail(url=member.avatar_url)
        await channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_message_edit(self, message_before, message_after):
        if message_before.channel.id == 955942097960181851:
            embed = disnake.Embed(
                description="ვიღაცამ დაარედაქტირა მესიჯი, შესაძლოა თამაშის გაფუჭებას ცდილობს! ყურადღებით "
                            "წაიკითხე დაბლა!", color=0x2d56a9)
            embed.add_field(name="დარედაქტირებული მესიჯი", value="%s" % message_after.content, inline=False)
            embed.add_field(name="ორიგინალური მესიჯი", value="%s" % message_before.content)
            embed.set_footer(text="დაარედაქტირა: %s" % message_before.author, icon_url=message_before.author.avatar_url)
            await message_before.channel.send(embed=embed)
        else:
            pass



def setup(client):
    client.add_cog(Events(client))
