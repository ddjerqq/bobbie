import random
import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction as Aci

from client.client import Client, GUILD_IDS


class FunCommands(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    @commands.user_command(name="gay", description="გაიგე რამდენად გეია შენ ან სხვა", guild_ids=GUILD_IDS)
    async def gay_user(self, inter: Aci, target: disnake.Member):
        embed = disnake.Embed(
            title="გეი ჰორმონების პროცენტის გამოცნობის მექანიზმი",
            color=0x2d56a9)

        embed.add_field(
            name="გეი ტესტის რეზულტატი",
            value=f"{inter.author.mention}'მ ჩაიტარა გეი გამოკვლების ტესტი და აღმოაჩინა რომ {target.mention} "
                  f"{random.randint(1, 100)} პროცენთით გეია 🏳️‍🌈.")

        await inter.send(embed=embed)

    @commands.slash_command(name="gay", description="გაიგე რამდენად გეია შენ ან სხვა", guild_ids=GUILD_IDS)
    async def gay_slash(self, inter: Aci, target: disnake.Member = None):
        target = target or inter.author

        embed = disnake.Embed(
            title="გეი ჰორმონების პროცენტის გამოცნობის მექანიზმი",
            color=0x2d56a9)

        embed.add_field(
            name="გეი ტესტის რეზულტატი",
            value=f"{inter.author.mention}'მ ჩაიტარა გეი გამოკვლების ტესტი და აღმოაჩინა რომ {target.mention} "
                  f"{round(random.gauss(50, 13))} პროცენთით გეია 🏳️‍🌈.")

        await inter.send(embed=embed)

    @commands.slash_command(name="avatar", description="გაადიდე user-ის ავატარი", guild_ids=GUILD_IDS)
    async def avatar_slash(self, inter: Aci, target: disnake.Member = None):
        target = target or inter.author

        embed = disnake.Embed(color=0x2d56a9)
        embed.add_field(
            name=f"{target.name}'ს ავატარი",
            value=f"ID: {target.id}")
        embed.set_image(url=target.avatar.url)

        await inter.send(embed=embed)

    @commands.user_command(name="avatar", description="გაადიდე user-ის ავატარი", guild_ids=GUILD_IDS)
    async def avatar_user(self, inter: Aci, target: disnake.Member):
        embed = disnake.Embed(color=0x2d56a9)
        embed.add_field(
            name=f"{target.name}'ს ავატარი",
            value=f"ID: {target.id}")
        embed.set_image(url=target.avatar.url)

        await inter.send(embed=embed)

    @commands.slash_command(name="info", description="გაიგეთ user-ის ინფო", guild_ids=GUILD_IDS)
    async def info_slash(self, inter: Aci, target: disnake.Member = None):
        target = target or inter.author
        embed = disnake.Embed(color=0x2d56a9)
        embed.add_field(
            name=f"{target.name}'ს ინფო",
            value=f"ID: {target.id}")
        embed.add_field(
            name="დაჯოინდა",
            value=target.joined_at.strftime("%d-%m-%Y"))
        embed.add_field(
            name=f"{target.name}'ს როლები",
            value=", ".join(map(lambda r: r.name, target.roles)),
            inline=False
        )

        embed.set_thumbnail(url=target.avatar.url)
        embed.set_footer(text="დარეგისტრირდა: " + target.created_at.strftime("%d-%m-%y %H:%M:%S"))

        await inter.send(embed=embed)

    @commands.slash_command(name="slap", description="გაულაწუნე ვინმეს", guild_ids=GUILD_IDS)
    async def slap_slash(self, inter: Aci, target: disnake.Member = None):
        target = target or inter.author
        embed = disnake.Embed(
            color=0x2d56a9,
            description=f"{inter.author.mention} გაბრაზდა და ძლიერად შემოულაწუნა {target.mention}'ს ✊"
        )
        await inter.send(embed=embed)

    @commands.slash_command(name="hug", description="ჩაეხუტე ვინმეს", guild_ids=GUILD_IDS)
    async def hug_slash(self, inter: Aci, target: disnake.Member = None):
        target = target or inter.author
        embed = disnake.Embed(
            color=0x2d56a9,
            description=f"{inter.author.mention} გულიანად ჩაეხუტა {target.mention}'ს <3"
        )
        await inter.send(embed=embed)

    @commands.slash_command(name="kiss", description="აკოცე ვინმეს", guild_ids=GUILD_IDS)
    async def kiss_slash(self, inter: Aci, target: disnake.Member = None):
        target = target or inter.author
        embed = disnake.Embed(
            color=0x2d56a9,
            description=f"{inter.author.mention}'მ აკოცა {target.mention}'ს <3"
        )
        await inter.send(embed=embed)

    @commands.slash_command(name="marry", description="დაქორწინდი ვინმეზე", guild_ids=GUILD_IDS)
    async def marry_slash(self, inter: Aci, target: disnake.Member = None):
        embed = disnake.Embed(
            color=0x2d56a9,
            description=f"{inter.author.mention} დაქორწინდა {target.mention}'ზე <3"
        )
        await inter.send(embed=embed)


def setup(client):
    client.add_cog(FunCommands(client))