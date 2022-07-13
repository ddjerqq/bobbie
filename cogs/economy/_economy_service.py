import disnake
from client.client import Client
from disnake import ApplicationCommandInteraction as Aci
from disnake.ext.commands import Context as Ctx


class EconomyService:
    def __init__(self, client: Client):
        self.__client = client

    async def balance(self, target: disnake.Member) -> disnake.Embed:
        """
        get users balance
        target.display_name's balance

        """
        user = await self.__client.db.users.get(target.id)

        em = disnake.Embed(
            color=target.color,
            title=f"{target.display_name}'ს ბალანსი"
        )
        em.add_field(name="ბანკი:",
                     value=f"{user.bank}₾")
        em.add_field(name="საფულე:",
                     value=f"{user.wallet}₾", inline=False)
        em.set_footer(icon_url=target.avatar.url, text=f"exp: {user.experience}")

        return em

    async def deposit(self, user: disnake.Member, amount: int) -> None:
        """
        Deposit money to user's bank
        we are assured that the amount is valid.
        because we have checks inside the Cog
        """
        user = await self.__client.db.users.get(user.id)

        # we can be sure that this works, because bobbie/cogs/economy/economy/check_has_enough_money
        # we are assured that the user has enough money.
        user.wallet -= amount
        user.bank   += amount
        user.experience += 3
        await self.__client.db.users.update(user)

    async def withdraw(self, user: disnake.Member, amount: int) -> None:
        """
        Withdraw money from user's bank
        same with deposit, we are sure that we have enough money
        """
        user = await self.__client.db.users.get(user.id)

        user.bank -= amount
        user.wallet += amount
        user.experience += 3
        await self.__client.db.users.update(user)

    async def give(self, sender: disnake.Member, receiver: disnake.Member, amount: int) -> None:
        """
        Give money to another user
        :param sender: user who gives money
        :param receiver: user who receives money
        :param amount: amount to give

        :return: None
        """
        this  = await self.__client.db.users.get(sender.id)
        other = await self.__client.db.users.get(receiver.id)

        if this.wallet   >= amount:
            this.wallet  -= amount
            other.wallet += amount

        this.experience += 5
        await self.__client.db.users.update(this)
        await self.__client.db.users.update(other)
