import disnake
from disnake.ext import commands
from disnake import ApplicationCommandInteraction as Aci

from client.client import Client, GUILD_IDS
from cogs._cog_services._fun_service import FunService


class FunCommands(commands.Cog):
    def __init__(self, client: Client):
        self.client = client
        self.fun_service = FunService(client)

    @commands.slash_command(name="gay", description="გაიგე რამდენად გეია შენ ან სხვა", guild_ids=GUILD_IDS)
    async def gay_slash(self, inter: Aci, target: disnake.Member = None):
        em = self.fun_service.gay(inter.author, target or inter.author)
        await inter.send(embed=em)

    @commands.command(name="gay")
    async def gay_text(self, ctx: commands.Context, target: disnake.Member = None):
        em = self.fun_service.gay(ctx.author, target or ctx.author)
        await ctx.send(embed=em)

    @commands.slash_command(name="slap", description="გაულაწუნე ვინმეს", guild_ids=GUILD_IDS)
    async def slap_slash(self, inter: Aci, target: disnake.Member = None):
        em = self.fun_service.slap(inter.author, target or inter.author)
        await inter.send(embed=em)

    @commands.command(name="slap")
    async def slap_text(self, ctx: commands.Context, target: disnake.Member = None):
        em = self.fun_service.slap(ctx.author, target or ctx.author)
        await ctx.send(embed=em)

    @commands.slash_command(name="hug", description="ჩაეხუტე ვინმეს", guild_ids=GUILD_IDS)
    async def hug_slash(self, inter: Aci, target: disnake.Member = None):
        em = self.fun_service.hug(inter.author, target or inter.author)
        await inter.send(embed=em)

    @commands.command(name="hug")
    async def hug_text(self, ctx: commands.Context, target: disnake.Member = None):
        em = self.fun_service.hug(ctx.author, target or ctx.author)
        await ctx.send(embed=em)

    @commands.slash_command(name="kiss", description="აკოცე ვინმეს", guild_ids=GUILD_IDS)
    async def kiss_slash(self, inter: Aci, target: disnake.Member = None):
        em = self.fun_service.kiss(inter.author, target or inter.author)
        await inter.send(embed=em)

    @commands.command(name="kiss")
    async def kiss_text(self, ctx: commands.Context, target: disnake.Member = None):
        em = self.fun_service.kiss(ctx.author, target or ctx.author)
        await ctx.send(embed=em)

    @commands.slash_command(name="coffee", description="დალიე ყავა", guild_ids=GUILD_IDS)
    async def coffee_slash(self, inter: Aci):
        em = self.fun_service.coffee(inter.author)
        await inter.send(embed=em)

    @commands.command(name="coffee")
    async def coffee_text(self, ctx: commands.Context):
        em = self.fun_service.coffee(ctx.author)
        await ctx.send(embed=em)

    @commands.slash_command(name="tea", description="დალიე ჩაი", guild_ids=GUILD_IDS)
    async def tea_slash(self, inter: Aci):
        em = self.fun_service.tea(inter.author)
        await inter.send(embed=em)

    @commands.command(name="tea")
    async def tea_text(self, ctx: commands.Context):
        em = self.fun_service.tea(ctx.author)
        await ctx.send(embed=em)

    @commands.slash_command(name="beer", description="დალიე ლუდი", guild_ids=GUILD_IDS)
    async def beer_slash(self, inter: Aci):
        em = self.fun_service.beer(inter.author)
        await inter.send(embed=em)

    @commands.command(name="beer")
    async def beer_text(self, ctx: commands.Context):
        em = self.fun_service.beer(ctx.author)
        await ctx.send(embed=em)

    @commands.slash_command(name="popcorn", description="შეჭამე პოპკრონორი", guild_ids=GUILD_IDS)
    async def popcorn_slash(self, inter: Aci):
        em = self.fun_service.popcorn(inter.author)
        await inter.send(embed=em)

    @commands.command(name="popcorn")
    async def popcorn_text(self, ctx: commands.Context):
        em = self.fun_service.popcorn(ctx.author)
        await ctx.send(embed=em)

    @commands.slash_command(name="fuck", description="მოტყანი ვინმე", guild_ids=GUILD_IDS)
    async def fuck_slash(self, inter: Aci, target: disnake.Member = None):
        em = self.fun_service.fuck(inter.author, target or inter.author)
        await inter.send(embed=em)

    @commands.command(name="fuck")
    async def fuck_text(self, ctx: commands.Context, target: disnake.Member = None):
        em = self.fun_service.fuck(ctx.author, target or ctx.author)
        await ctx.send(embed=em)


def setup(client):
    client.add_cog(FunCommands(client))
