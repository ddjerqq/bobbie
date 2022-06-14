from disnake.ext import commands
from disnake.ext.commands import errors
from disnake import ApplicationCommandInteraction as Aci
from disnake.ext.commands import Context as Ctx

from client.client import Client, DEV_TEST, GUILD_IDS
from client.logger import LogLevel
from cogs._cog_services._pet_service import PetService
from database.enums import *


class PetSystemCommands(commands.Cog):
    def __init__(self, client: Client):
        self.client = client
        self.pet_service = PetService(client)

    # region COMMAND BUY
    @commands.slash_command(name="buy_pet", guild_ids=GUILD_IDS, description="იყიდე რაიმე ცხოველი მაღაზიიდან")
    @commands.cooldown(1, 3600 if not DEV_TEST else 1, commands.BucketType.user)
    async def buy_slash(self, inter: Aci, item: PET_BUY_PRICES):  # treat item as item slug
        em = await self.pet_service.buy(inter.author, item)
        await inter.send(embed=em)
    # endregion

    # region COMMAND PETS
    @commands.slash_command(name="pet_inventory", guild_ids=GUILD_IDS, description="ნახე შენი შინაური ცხოველები")
    async def pet_inventory_slash(self, inter: Aci):
        em = await self.pet_service.inventory(inter.author)
        await inter.send(embed=em)

    @commands.command(name="pet_inventory")
    async def pet_inventory_text(self, ctx: Ctx):
        em = await self.pet_service.inventory(ctx.author)
        await ctx.send(embed=em)


def setup(client):
    client.add_cog(PetSystemCommands(client))
