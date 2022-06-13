import random

import disnake
from disnake import ApplicationCommandInteraction as Aci
from disnake.ext import commands

from client.client import Client
from database import ItemType


class FunService:
    def __init__(self, client: Client):
        self.__client = client

    def gay(self, sender: disnake.Member, target: disnake.Member) -> disnake.Embed:
        em = disnake.Embed(
            title="გეი ჰორმონების პროცენტის გამოცნობის მექანიზმი",
            color=0x2d56a9)

        em.add_field(
            name="გეი ტესტის რეზულტატი",
            value=f"{sender.mention}'მ ჩაიტარა გეი გამოკვლების ტესტი და აღმოაჩინა რომ {target.mention} "
                  f"{random.randint(1, 100)} პროცენთით გეია 🏳️‍🌈.")

        return em

    def slap(self, user: disnake.Member, target: disnake.Member) -> disnake.Embed:
        em = disnake.Embed(
            color=0x2d56a9,
            description=f"{user.mention} გაბრაზდა და ძლიერად შემოულაწუნა {target.mention}'ს ✊"
        )
        return em

    def hug(self, user: disnake.Member, target: disnake.Member) -> disnake.Embed:
        em = disnake.Embed(
            color=0x2d56a9,
            description=f"{user.mention} გულიანად ჩაეხუტა {target.mention}'ს <3"
        )
        return em

    def kiss(self, user: disnake.Member, target: disnake.Member) -> disnake.Embed:
        em = disnake.Embed(
            color=0x2d56a9,
            description=f"{user.mention}'მ აკოცა {target.mention}'ს <3"
        )
        return em

    def coffee(self, user: disnake.Member) -> disnake.Embed:
        coffee_types = [
            "კაპუჩინო",
            "მოკა",
            "ბობა"
        ]
        em = self.__client.embeds.generic.generic_success(
            title=f"{user.mention}'მ დალია {random.choice(coffee_types)} ყავა",
        )
        return em

    def tea(self, user: disnake.Member) -> disnake.Embed:
        tea_types = [
            "მწვანე",
            "შავი",
            "ტყის",
            "კენკრის",
            "მოცვის",
            "მოცოცვის"
        ]
        em = self.__client.embeds.generic.generic_success(
            title=f"{user.mention}'მ დალია {random.choice(tea_types)} ჩაი",
        )

        return em

    def beer(self, user: disnake.Member) -> disnake.Embed:
        beer_types = [
            "ბავარიული",
            "შავი",
            "ავსტრიული",
            "ჩამოსასხმელი",
            "ნატახტარის",
            "ზედაზენის"
        ]
        em = self.__client.embeds.generic.generic_success(
            title=f"{user.mention}'მ დალია {random.choice(beer_types)} ლუდი"
        )

        return em

    def popcorn(self, user: disnake.Member) -> disnake.Embed:
        em = self.__client.embeds.generic.generic_success(
            title=f"{user.mention}'მ საიდანღაც დააძრო პოპკორნი"
        )
        return em

    def fuck(self, user: disnake.Member, target: disnake.Member) -> disnake.Embed:
        em = disnake.Embed(
            color=0x2d56a9,
            description=f"{user.mention}'მ მაგრად მოტყნა {target.mention}"
        )
        return em


    async def marry(self, inter: Aci | commands.Context, target: disnake.Member) -> None:
        user = await self.__client.db.users.get(inter.author.id)
        ring = next((item for item in user.items if item.type == ItemType.WEDDING_RING), None)

        if not ring:
            em = self.__client.embeds.generic.generic_error(
                title="დებილო მაიმუნო ბავშვო შენა!!",
                description=f"შენ ვერ მოიყვან {target.mention}'ს ცოლად რადგან არ გაქვს საქორწინო ბეჭედი.\n"
                            f"ფული შეაგროვე და იყიდე მაღაზიაში!!")
            await inter.send(embed=em)
            return

        yes_no = self.__client.embeds.utils.confirmation_needed(f"{inter.author.name}-ზე დაქორწინება, {target.mention}")
        button = self.__client.buttons.YesNoButton(target)

        await inter.send(embed=yes_no, view=button)
        result = await button.wait()

        if result:
            user.items.remove(ring)

            em = self.__client.embeds.generic.generic_success(
                title="გილოცავთ!🎂🍰💒",
                description=f"🤵{inter.author.mention} და 👰{target.mention} დაქორწინდნენ 🎊🎊🎊🎊"
            )

        else:
            em = self.__client.embeds.generic.generic_error(
                title=f"არაო 😐😒😔😕",
                description=f"{target.mention}'ს არ უნდა შენზე დაქორწინება, \n"
                            f"||თქვა რო ყლეაო და არ მევასებაო ahahhahah||"
            )

        await inter.send(embed=em)
