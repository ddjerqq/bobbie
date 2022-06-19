import random

import disnake
from disnake import ApplicationCommandInteraction as Aci
from disnake.ext import commands

from client.client import Client
from database import ItemType
from database.factories.marriage_factory import MarriageFactory


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
            title=f"{user.name}'მ დალია {random.choice(coffee_types)} ყავა",
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
            title=f"{user.name}'მ დალია {random.choice(tea_types)} ჩაი",
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
            title=f"{user.name}'მ დალია {random.choice(beer_types)} ლუდი"
        )

        return em

    def popcorn(self, user: disnake.Member) -> disnake.Embed:
        em = self.__client.embeds.generic.generic_success(
            title=f"{user.name}'მ საიდანღაც დააძრო პოპკორნი"
        )
        return em

    def fuck(self, user: disnake.Member, target: disnake.Member) -> disnake.Embed:
        em = disnake.Embed(
            color=0x2d56a9,
            description=f"{user.mention}'მ მაგრად მოტყნა {target.mention}"
        )
        return em

    stuff = set()
    async def marry(self, inter: Aci, target: disnake.Member, stuff=stuff) -> None:
        
        if not inter.author in stuff:
            stuff.add(inter.author)
        elif inter.author in stuff:
            return
        
        if target.bot:
            em = self.__client.embeds.generic.generic_error(
                title="დებილო მაიმუნო ბავშვო შენა!!",
                description=f"შენ ვერ მოიყვან რობოტს ცოლად")
            await inter.send(embed=em)
            return


        user        = await self.__client.db.users.get(inter.author.id)
        target_user = await self.__client.db.users.get(target.id)
        ring        = next((item for item in user.items if item.type == ItemType.WEDDING_RING), None)

        if user and user.marriage_id is not None:
            marriage = await self.__client.db.marriages.get(user.marriage_id)

            if not marriage:
                user.marriage_id = None

            if marriage and user.id == marriage.bride_id:
                married_to = self.__client.get_user(marriage.king_id)
            elif marriage and user.id == marriage.king_id:
                married_to = self.__client.get_user(marriage.bride_id)
            if marriage:
                em = self.__client.embeds.generic.generic_error(
                    title="დებილო მაიმუნო ბავშვო შენა!!",
                    description=f"შენ უკვე დაქორწინებული ხარ {married_to.mention}. განქორწინდი მისგან თუ გინდა ახალი ცოლი.")
                await inter.send(embed=em)
                return

        if not ring:
            em = self.__client.embeds.generic.generic_error(
                title="დებილო მაიმუნო ბავშვო შენა!!",
                description=f"შენ ვერ მოიყვან {target.mention}'ს ცოლად რადგან არ გაქვს საქორწინო ბეჭედი.\n"
                            f"ფული შეაგროვე და იყიდე მაღაზიაში!!")
            await inter.send(embed=em)
            return

        if target.id == inter.author.id:
            em = self.__client.embeds.generic.generic_error(
                title="დებილო მაიმუნო ბავშვო შენა 🤡",
                description=f"შენ ვერ მოიყვან შენს თავს ცოლად!!")
            await inter.send(embed=em)
            return
        

        yes_no = self.__client.embeds.utils.confirmation_needed(f"{target.mention}, თანახმა ხართ თუ არა რომ ცოლად გაყვეთ {inter.author.mention}ს, მზად ხართ რომ ჭირშიც და ლხინშიც მის გვერით იყოთ?")
        button = self.__client.buttons.YesNoButton(intended_user=target, timeout=600)

        await inter.send(embed=yes_no, view=button)
        await button.wait()

        if not button.choice:
            em = self.__client.embeds.generic.generic_error(
                title=f"არაო 😐😒😔😕🤡🤡🤡🤡",
                description=f"{target.mention}'ს არ უნდა შენზე დაქორწინება")
            stuff.remove(inter.author)
            await inter.edit_original_message(embed=em, view=None)

        user.items.remove(ring)

        color = random.randint(0, 0xffffff)
        bride_role = await inter.guild.create_role(name=f"{inter.author.name}'ს ცოლი",
                                                   color=color,
                                                   reason="Marriage")
        king_role  = await inter.guild.create_role(name=f"{target.name}'ს ქმარი",
                                                   color=color,
                                                   reason="Marriage")
        marriage = MarriageFactory.new(inter.author, target, inter.guild, bride_role, king_role)
        await self.__client.db.marriages.add(marriage)

        await inter.author.add_roles(king_role, reason="Marriage")
        await target.add_roles(bride_role, reason="Marriage")

        user.marriage_id = marriage.id
        target_user.marriage_id = marriage.id

        await self.__client.db.users.update(user)
        await self.__client.db.users.update(target_user)

        em = self.__client.embeds.generic.generic_success(
            title="გილოცავთ! 🎂🍰💒",
            description=f"მონიჭებული უფლებით, 🤵{inter.author.mention} და 👰{target.mention} გაცხადებთ ცოლ-ქმრად,შეგიძლიად ერთმანეთს აკოცოთ. (/kiss)"
        )
        stuff.remove(inter.author)
        await inter.edit_original_message(embed=em, view=None)


    async def divorce(self, inter: Aci | commands.Context) -> None:
        user = await self.__client.db.users.get(inter.author.id)

        if not user.marriage_id:
            em = self.__client.embeds.generic.generic_success(
                title="დებილო მაინმუნო ბავშვო შენა!",
                description=f"შენ არც ხარ არავისზე დაქორწინებული. ვერავისაც ვერ გაეყრები 😒😐"
            )
            await inter.send(embed=em)
            return


        marriage = await self.__client.db.marriages.get(user.marriage_id)

        guild = self.__client.get_guild(marriage.guild_id)
        bride_role = guild.get_role(marriage.bride_role_id)
        king_role  = guild.get_role(marriage.king_role_id)
        await bride_role.delete(reason="Divorce")
        await king_role.delete(reason="Divorce")

        user.marriage_id = None
        if user.id == marriage.bride_id:
            married_to = await self.__client.db.users.get(marriage.king_id)
            married_to.marriage_id = None
        else:
            married_to = await self.__client.db.users.get(marriage.bride_id)
            married_to.marriage_id = None
        await self.__client.db.users.update(user)
        await self.__client.db.users.update(married_to)
        # await self.__client.db.marriages.delete(marriage)

        married_to_member = guild.get_member(married_to.id)
        em = self.__client.embeds.generic.generic_success(
            title="წარმატება! 📃",
            # check who is the bride and who is the king
            description=f"{inter.author.mention} და {married_to_member.mention} განქორწინდნენ"
        )

        await inter.send(embed=em)
