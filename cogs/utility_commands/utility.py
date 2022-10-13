import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction as Aci


from client.client import Client, GUILD_IDS
from cogs._cog_services._utility_service import UtilityService


class UtilityCommands(commands.Cog):
    def __init__(self, client: Client):
        self.client = client
        self.util_service = UtilityService(client)


    @commands.slash_command(name="avatar", description="გაადიდე user-ის ავატარი", guild_ids=GUILD_IDS)
    async def avatar_slash(self, inter: Aci, target: disnake.Member = None):
        em = self.util_service.avatar(target or inter.author)
        await inter.send(embed=em)


    @commands.command(name="avatar")
    async def avatar_text(self, ctx: commands.Context, target: disnake.Member = None):
        em = self.util_service.avatar(target or ctx.author)
        await ctx.send(embed=em)


    @commands.slash_command(name="info", description="გაიგეთ მომხმარებლის ინფო", guild_ids=GUILD_IDS)
    async def info_slash(self, inter: Aci, target: disnake.Member = None):
        em = self.util_service.info(target or inter.author)
        await inter.send(embed=em)


    @commands.command(name="info")
    async def info_text(self, ctx: commands.Context, target: disnake.Member = None):
        em = self.util_service.info(target or ctx.author)
        await ctx.send(embed=em)

    @commands.slash_command(name="ping", description="ბოტის რეაქციის დრო", guild_ids=GUILD_IDS)
    async def ping_slash(self, inter: Aci):
        em = self.util_service.ping()
        await inter.send(embed=em)

    @commands.command(name="ping")
    async def ping_text(self, ctx: commands.Context):
        em = self.util_service.ping()
        await ctx.send(embed=em)


def setup(client):
    client.add_cog(UtilityCommands(client))
