import random

import disnake
from disnake import ApplicationCommandInteraction as Aci

from client.client import Client
from database import ItemType
from database.factories.marriage_factory import MarriageFactory


class MarriageService:
    def __init__(self, client: Client):
        self.__client = client

    async def marry(self, inter: Aci, target_member: disnake.Member) -> None:
        user   = await self.__client.db.users.get(inter.author.id)
        target = await self.__client.db.users.get(target_member.id)
        ring   = next((it for it in user.items if it.type == ItemType.WEDDING_RING), None)

        yes_no = self.__client.embeds.utils.confirmation_needed(
            f"{inter.author.mention}-ზე დაქორწინება, <@{target.id}>"
        )
        button = self.__client.buttons.YesNoButton(
            intended_user=target,
            timeout=600,
        )

        await inter.send(embed=yes_no, view=button)
        await button.wait()

        if not button.choice:
            em = self.__client.embeds.generic.generic_error(
                title=f"არაო 😐😒😔😕🤡🤡🤡🤡",
                description=f"{target.mention}'ს არ უნდა შენზე დაქორწინება ||ყლეაო და მაგიტოო :(||"
            )
            await inter.edit_original_message(embed=em, view=None)
            return

        # success logic
        user.items.remove(ring)
        ring.owner_id = target.id
        target.items.append(ring)
        color = random.randint(0, 0xffffff)
        bride_role = await inter.guild.create_role(
            name=f"{inter.author.name}'ს ცოლი",
            color=color,
            reason="Marriage"
        )
        king_role  = await inter.guild.create_role(
            name=f"{target.username}'ს ქმარი",
            color=color,
            reason="Marriage"
        )

        marriage = MarriageFactory.new(inter.author, target, inter.guild, bride_role, king_role)
        await self.__client.db.marriages.add(marriage)

        await inter.author.add_roles(king_role, reason="Marriage")
        await target_member.add_roles(bride_role, reason="Marriage")

        user.marriage_id   = marriage.id
        target.marriage_id = marriage.id

        await self.__client.db.users.update(user)
        await self.__client.db.users.update(target)

        em = self.__client.embeds.generic.generic_success(
            title="გილოცავთ! 🎂🍰💒",
            description=f"🤵{inter.author.mention} და 👰<@{target.id}> დაქორწინდნენ 🎊🎊🎊🎊"
        )
        await inter.edit_original_message(embed=em, view=None)


    async def divorce(self, inter: Aci) -> None:
        # get junk
        user = await self.__client.db.users.get(inter.author.id)
        marriage = await self.__client.db.marriages.get(user.marriage_id)

        married_to_id = marriage.king_id if user.id == marriage.bride_id else marriage.bride_id
        target = await self.__client.db.users.get(married_to_id)

        # discord dependencies
        guild = self.__client.get_guild(marriage.guild_id)
        bride_role = guild.get_role(marriage.bride_role_id)
        king_role  = guild.get_role(marriage.king_role_id)

        # clean up roles
        if bride_role:
            await bride_role.delete(reason="Divorce")
        if king_role:
            await king_role.delete(reason="Divorce")

        # clear marriages from the database
        user.marriage_id = None
        target.marriage_id = None

        await self.__client.db.users.update(user)
        await self.__client.db.users.update(target)
        await self.__client.db.marriages.delete(marriage)

        em = self.__client.embeds.generic.generic_success(
            title="წარმატება! 📃",
            # check who is the bride and who is the king
            description=f"{inter.author.mention} და <@{target.id}> განქორწინდნენ"
        )

        await inter.send(embed=em)
