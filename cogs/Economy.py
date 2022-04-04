import disnake
from disnake.ext import commands
from disnake.ext.commands import errors
from disnake import ApplicationCommandInteraction as Aci

from utils import *
from services import user_service


class Economy(commands.Cog):
    def __init__(self, client: disnake.Client):
        self.client = client


    @commands.slash_command(name="balance", guild_ids=GUILD_IDS, description="გაიგე რამდენი ფული გაქვს")
    async def balance_slash(self, inter: Aci, target: disnake.Member = None):
        target = target or inter.author
        await self.balance_usercom(inter, target)


    @commands.user_command(name="bal", description="user-ის ბალანსი", guild_ids=GUILD_IDS)
    async def balance_usercom(self, inter: Aci, target: disnake.Member):

        bank, wallet = await user_service.get_user_balance(target.id)

        embed = disnake.Embed(
            title = f"{target.name}'ს ბალანსი <:money:960131849055764510>",
            color = 0x2d56a9)

        embed.add_field(
            name = "ბანკი",
            value = f"{bank}")

        embed.add_field(
            name = "საფულე",
            value = f"{wallet}")

        await inter.send(embed=embed)


    @commands.slash_command(name="deposit", guild_ids=GUILD_IDS, description="გადარიცხეთ თანხა საფულიდან ბანკში")
    async def deposit_slash(self, inter: Aci, amount: int):
        res = await user_service.deposit(inter.author.id, amount)
        if res:
            embed = disnake.Embed(
                color=0x00ff00,
                description="წარმატებით შეიტანეთ ბანკში თანხა")
        else:
            embed = disnake.Embed(
                color=0xff0000,
                description="თანხის შეტანა ვერ მოხერხდა, სავარაუდოდ საფულეში არასაკმარისი ფული გიდევს")

        await inter.send(embed=embed)


    @commands.slash_command(name = "withdraw", guild_ids = GUILD_IDS, description = "გამოიტანე ფული ბანკიდან საფულეში")
    async def withdraw_slash(self, inter: Aci, amount: int):
        res = await user_service.withdraw(inter.author.id, amount)
        if res:
            embed = disnake.Embed(
                color = 0x00ff00,
                description = "წარმატებით გაიტანეთ თანხა")
        else:
            embed = disnake.Embed(
                color = 0xff0000,
                description = "თანხის გატანა ვერ მოხერხდა, სავარაუდოდ საფულეში არასაკმარისი ფული გიდევს")

        await inter.send(embed = embed)


    @commands.slash_command(name="give", guild_ids=GUILD_IDS, description="მიეც გლახაკთა საჭურჭლე, ათავისუფლე მონები")
    async def give_slash(self, inter: Aci, target: disnake.Member, amount: int):
        user = await user_service.get_by_id(target.id)
        if user is None:
            embed = disnake.Embed(
                color=0xff0000,
                title=f"user-ი ვერ მოიძებნა",
                description=f"{target.mention} არ არსებობს")
            await inter.send(embed=embed)
            return

        if await user_service.give(inter.author.id, target.id, amount):
            embed = disnake.Embed(
                color = 0x00ff00,
                description = f"შენ წარმატებით მიეცი {target.name}'ს {amount} ₾")
        else:
            embed = disnake.Embed(
                color = 0x00ff00,
                desctiption = f"შენ არ გაქვს საკმარისი ფული ჯიბეში",
                description = f"შენ ვერ მიცემ {target.name}'ს {amount} ₾ს"
            )

        await inter.send(embed=embed)


    @commands.slash_command(name="work", guild_ids=GUILD_IDS, description="იმუშავე და გააკეთე 10 ₾არი")
    @commands.cooldown(1, 60, commands.BucketType.user)
    async def work_slash(self, inter: Aci):
        await user_service.work(inter.author.id)
        embed = disnake.Embed(
            description="შენ იმუშავე და გააკეთე 10 ₾არი <:hammer~1:960423335437680692>",
            color=0x00ff00
        )
        await user_service.give_exp(inter.author.id, 3)
        await inter.send(embed=embed)

    @work_slash.error
    async def _work_error(self, ctx: commands.Context, _error: errors.CommandError):
        if isinstance(_error, errors.CommandOnCooldown):
            embed = disnake.Embed(
                color=0xFF0000,
                title=f"ნელა ზვიადი",
                description=f"შენ უკვე იმუშავე, შენ შეძლებ ისევ მუშაობას {_error.retry_after:.1f} წამში")
            await ctx.send(embed=embed)

        else:
            await log_error(_error)


def setup(client):
    client.add_cog(Economy(client))
