import disnake
from disnake.ext import commands
from utils import *
from services.user_service import *


class Events(commands.Cog):
    def __init__(self, client: disnake.Client):
        self.client = client


    @commands.Cog.listener()
    async def on_close(self):
        print("closing")


    @commands.Cog.listener()
    async def on_ready(self):
        log("bobbi online")

        for guild in self.client.guilds:
            for user in guild.members:
                if not await database.users.exists(user.id) and not user.bot:
                    await add_user(user.id, user.name, user.joined_at)


    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        await add_xp(message.author.id, 1)


    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        await add_user(member.id, member.name, member.joined_at)
        # greet user an rame maseti


    @commands.Cog.listener()
    async def on_message_delete(self, message):
        channel = self.client.get_channel(939534645798793247)
        msg_content = message.content
        msg_author = message.author
        author_id = message.author.id
        embed = disnake.Embed(title="Bobbie's Archives", description="ბობიმ შეამჩნია წაშლილი მესიჯი მაგრამ მოასწრო "
                                                                     "სქრინის გადაღება!", color=0x2d56a9)
        embed.add_field(name="ავტორი", value="%s" % msg_author.mention, inline=True)
        embed.add_field(name="ID", value="%s" % author_id, inline=True)
        embed.add_field(name="მესიჯი", value="%s" % msg_content, inline=False)
        words = ["!gay", "!coffee", "!tea", "!hug", "!beer", "?ban", "?kick", "?purge", "?mute", "?unmute", "!slap", "!popcorn"]
        if any(word in msg_content for word in words):
            pass
        elif msg_author == 933243840905769040:
            pass
        else:
            await channel.send(embed=embed)


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
