from __future__ import annotations
import disnake
from database import ItemType
from disnake.ext import commands
from client.logger import LogLevel
from client.client import Client, GUILD_IDS
from disnake.ext.commands import CheckFailure
from disnake import ApplicationCommandInteraction as Aci
from cogs._cog_services._marriage_service import MarriageService


class TargetBot(CheckFailure):...
class MarriageSelfMarriage(CheckFailure):...
class MarriageAuthorHasNoRing(CheckFailure):...
class DivorceAuthorIsNotMarried(CheckFailure):...
class MarriageAuthorAlreadyMarried(CheckFailure):...
class MarriageTargetAlreadyMarried(CheckFailure):...


async def check_marriage_target_not_bot(inter: Aci) -> bool:
    target = inter.filled_options.get("target", None)
    if target.bot:
        raise TargetBot()
    return True


async def check_marriage_target_not_self(inter: Aci) -> bool:
    target = inter.filled_options.get("target", None)
    if target == inter.author:
        raise MarriageSelfMarriage()
    return True


async def check_marriage_author_has_ring(inter: Aci) -> bool:
    client: Client = inter.bot  # type: ignore
    user = await client.db.users.get(inter.author.id)
    if not any(it.type == ItemType.WEDDING_RING for it in user.items):
        raise MarriageAuthorHasNoRing()
    else:
        return True


async def check_marriage_author_is_not_married_already(inter: Aci) -> bool:
    client: Client = inter.bot  # type: ignore
    user = await client.db.users.get(inter.author.id)
    if user.marriage_id:
        raise MarriageAuthorAlreadyMarried()
    return True


async def check_marriage_target_is_not_married_already(inter: Aci) -> bool:
    client: Client = inter.bot  # type: ignore
    target = inter.filled_options.get("target", None)
    target = await client.db.users.get(target.id)
    if target.marriage_id:
        raise MarriageTargetAlreadyMarried()
    return True


async def check_divorce_author_is_married_already(inter: Aci) -> bool:
    client: Client = inter.bot  # type: ignore
    user = await client.db.users.get(inter.author.id)
    if not user.marriage_id:
        raise DivorceAuthorIsNotMarried()
    return True




class MarriageCommands(commands.Cog):
    def __init__(self, client: Client):
        self.client = client
        self.service = MarriageService(client)

    async def cog_slash_command_error(self, inter: Aci, error: commands.CommandError) -> bool:
        if isinstance(error, TargetBot):
            await inter.send(embed=self.client.embeds.generic.generic_error(
                title="დებილო მაიმუნო ბავშვო შენა!!!",
                description="შენ ვერ მოიყვან რობოტს ცოლად",
            ))
        elif isinstance(error, MarriageSelfMarriage):
            await inter.send(embed=self.client.embeds.generic.generic_error(
                title="დებილო მაიმუნო ბავშვო შენა!!!",
                description="შენ ვერ მოიყვან შენ თავს ცოლად",
            ))
        elif isinstance(error, MarriageAuthorHasNoRing):
            await inter.send(embed=self.client.embeds.generic.generic_error(
                title="დებილო მაიმუნო ბავშვო შენა!!!",
                description="შენ ხარ ღარიბი მაიმუნი ბავშვი, წადი მაღაზიაში და იყიდე ბეჭედი",
            ))
        elif isinstance(error, MarriageAuthorAlreadyMarried):
            await inter.send(embed=self.client.embeds.generic.generic_error(
                title="დებილო მაიმუნო ბავშვო შენა!!!",
                description="ღალატი არის სირებისთვის, შენ უკვე დაქორწინებული ხარ!!!!\n"
                            "განქორწინდი და მერე მოენძრიე!!!",
                ))
        elif isinstance(error, MarriageTargetAlreadyMarried):
            await inter.send(embed=self.client.embeds.generic.generic_error(
                title="დებილო მაიმუნო ბავშვო შენა!!!",
                description="ვაუ, რა ყლეობას აკეთებ, შენ ვერ მოიყვან დაქორწინებულ ადამიანს ცოლად\n"
                            "ასეთ დებილობას 8 წლის ბავშვიც კი არ იზავდა.",
                ))
        elif isinstance(error, DivorceAuthorIsNotMarried):
            await inter.send(embed=self.client.embeds.generic.generic_error(
                title="დებილო მაიმუნო ბავშვო შენა!!!",
                description="ვიზე უნდა განქორწინდე, ცხოვრებაში არავის უნდოდი და არც ხარ დაქორწინებული!!",
            ))
        else:
            await self.client.logger.log(f"{error!r}", level=LogLevel.ERROR)
            return False

        return True

    @commands.user_command(name="marry", description="დაქორწინდი ვინმეზე", guild_ids=GUILD_IDS)
    @commands.check(check_marriage_target_is_not_married_already)
    @commands.check(check_marriage_author_is_not_married_already)
    @commands.check(check_marriage_author_has_ring)
    @commands.check(check_marriage_target_not_self)
    @commands.check(check_marriage_target_not_bot)
    async def marry_user(self, inter: Aci, target: disnake.Member):
        await self.service.marry(inter, target)

    @commands.slash_command(name="marry", description="დაქორწინდი ვინმეზე", guild_ids=GUILD_IDS)
    @commands.check(check_marriage_target_is_not_married_already)
    @commands.check(check_marriage_author_is_not_married_already)
    @commands.check(check_marriage_author_has_ring)
    @commands.check(check_marriage_target_not_self)
    @commands.check(check_marriage_target_not_bot)
    async def marry_slash(self, inter: Aci, target: disnake.Member):
        await self.service.marry(inter, target)

    @commands.slash_command(name="divorce", description="განქორწინება", guild_ids=GUILD_IDS)
    @commands.check(check_divorce_author_is_married_already)
    async def divorce_slash(self, inter: Aci):
        await self.service.divorce(inter)


def setup(client: Client):
    client.add_cog(MarriageCommands(client))
