import random
import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction as Aci

from utils import *
from client import Client


class ApplicationCommands(commands.Cog):
    def __init__(self, client: Client):
        self.confession_channel: disnake.TextChannel | None = None
        self.client = client

    @commands.user_command(name="gay", description="გაიგე რამდენად გეია შენ ან სხვა", guild_ids=GUILD_IDS)
    async def gay(self, inter: Aci, target: disnake.Member):
        embed = disnake.Embed(
            title="გეი ჰორმონების პროცენტის გამოცნობის მექანიზმი",
            color=0x2d56a9)

        embed.add_field(
            name="გეი ტესტის რეზულტატი",
            value=f"{inter.author.mention}'მ ჩაიტარა გეი გამოკვლების ტესტი და აღმოაჩინა რომ {target.mention} "
                  f"{random.randint(1, 100)} პროცენთით გეია 🏳️‍🌈.")

        await inter.send(embed=embed)

    @commands.user_command(name="avatar", description="გაადიდე user-ის ავატარი", guild_ids=GUILD_IDS)
    async def avatar(self, inter: Aci, target: disnake.Member):
        embed = disnake.Embed(color=0x2d56a9)
        embed.add_field(
            name=f"{target.name}'ს ავატარი",
            value=f"ID: {target.id}")
        embed.set_image(url=target.avatar.url)

        await inter.send(embed=embed)

    @commands.user_command(name="bal", guild_ids=GUILD_IDS, description="user-ის ბალანსი")
    async def balance(self, inter: Aci, target: disnake.Member):
        em = await self.client.embeds.econ_util_balance(target)
        await inter.send(embed=em)


def setup(client):
    client.add_cog(ApplicationCommands(client))
