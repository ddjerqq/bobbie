import random

import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction as Aci

from utils import *


class ApplicationCommands(commands.Cog):
    def __init__(self, client):
        self.client = client


    @commands.slash_command(name="gay", guild_ids=GUILD_IDS, description="გაიგე რამდენად გეია შენ ან სხვა")
    async def gay_slash(self, inter: Aci, target: disnake.Member = None):
        target = target or inter.author
        await self.gay_usercom(inter, target)


    @commands.user_command(name="gay", description="გაიგე რამდენად გეია შენ ან სხვა", guild_ids=GUILD_IDS)
    async def gay_usercom(self, inter: Aci, target: disnake.Member):
        embed = disnake.Embed(
            title = "გეი ჰორმონების პროცენტის გამოცნობის მექანიზმი",
            color = 0x2d56a9)

        embed.add_field(
            name = "გეი ტესტის რეზულტატი",
            value = f"{inter.author.mention}'მ ჩაიტარა გეი გამოკვლების ტესტი და აღმოაჩინა რომ {target.mention} "
                    f"{random.randint(1, 100)} პროცენთით გეია 🏳️‍🌈.")

        await inter.send(embed=embed)


    @commands.slash_command(name="avatar", description="გაადიდე user-ის ავატარი", guild_ids=GUILD_IDS)
    async def avatar_slash(self, inter: Aci, target: disnake.Member = None):
        target = target or inter.author
        await self.avatar_usercom(inter, target)


    @commands.user_command(name="avatar", description="გაადიდე user-ის ავატარი", guild_ids=GUILD_IDS)
    async def avatar_usercom(self, inter: Aci, target: disnake.Member):
        embed = disnake.Embed(color=0x2d56a9)
        embed.add_field(
            name=f"{target.mention}'ს ავატარი",
            value=f"ID: {target.id}")
        embed.set_image(url=target.avatar.url)

        await inter.send(embed=embed)


    @commands.slash_command(name="info", description="გაიგეთ user-ის ინფო", guild_ids=GUILD_IDS)
    async def info_slash(self, inter: Aci, target: disnake.Member = None):
        target = target or inter.author
        await self.info_usercom(inter, target)


    @commands.user_command(name="info", description="გაიგეთ user-ის ინფო", guild_ids=GUILD_IDS)
    async def info_usercom(self, inter: Aci, target: disnake.Member):
        embed = disnake.Embed(color = 0x2d56a9)
        embed.add_field(
            name = f"{target.mention}'ს ინფო",
            value = f"ID: {target.id}")
        embed.add_field(
            name = "დაჯოინდა",
            value = target.joined_at.strftime("%d-%M-%Y"))
        embed.add_field(
            name = f"{target.mention}'ს როლები",
            value = ", ".join(map(lambda r: r.name, target.roles))
        )

        embed.set_thumbnail(url = target.avatar.url)
        embed.set_footer(text = "დარეგისტრირდა: " + target.created_at.strftime("%d-%m-%y %H:%M:%S"))

        await inter.send(embed = embed)


    @commands.slash_command(name="slap", guild_ids=GUILD_IDS, description="გაულაწუნე ვინმეს")
    async def slap_slash(self, inter: Aci, target: disnake.Member = None):
        target = target or inter.author
        await self.slap_usercom(inter, target)


    @commands.user_command(name="slap", guild_ids=GUILD_IDS, description="გაულაწუნე ვინმეს")
    async def slap_usercom(self, inter: Aci, target: disnake.Member):
        embed = disnake.Embed(
            color=0x2d56a9,
            description=f"{inter.author.mention} გაბრაზდა და ძლიერად შემოულაწუნა {target.mention}'ს ✊"
        )
        await inter.send(embed=embed)


    @commands.slash_command(name = "hug", guild_ids = GUILD_IDS, description = "ჩაეხუტე ვინმეს")
    async def hug_slash(self, inter: Aci, target: disnake.Member = None):
        target = target or inter.author
        await self.hug_usercom(inter, target)


    @commands.user_command(name = "hug", guild_ids = GUILD_IDS, description = "ჩაეხუტე ვინმეს")
    async def hug_usercom(self, inter: Aci, target: disnake.Member):
        embed = disnake.Embed(
            color = 0x2d56a9,
            description = f"{inter.author.mention} გულიანად ჩაეხუტა {target.mention}'ს <3"
        )
        await inter.send(embed = embed)


def setup(client):
    client.add_cog(ApplicationCommands(client))
