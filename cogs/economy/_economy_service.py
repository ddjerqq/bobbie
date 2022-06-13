import disnake
from client.client import Client


class EconomyService:
    def __init__(self, client: Client):
        self.__client = client

    async def balance(self, user: disnake.Member) -> disnake.Embed:
        """
        Check user's balance
        :param user: user to check balance of

        :return: disnake.Embed
        """
        em = await self.__client.embeds.economy.balance(user)
        return em

    async def deposit(self, user: disnake.Member, amount: str) -> disnake.Embed:
        """
        Deposit money to user's bank
        :param user: user to deposit money to
        :param amount: amount to deposit

        :return: disnake.Embed
        """
        user = await self.__client.db.users.get(user.id)

        if amount.isnumeric() and int(amount):
            amount = int(amount)
        elif amount in ["max", "all", "სულ"]:
            amount = user.wallet
        else:
            return self.__client.embeds.economy.error_invalid_amount_entered()

        if user.wallet >= amount:
            user.wallet -= amount
            user.bank += amount
            await self.__client.db.users.update(user)
            return self.__client.embeds.economy.success_deposit(user, amount)

        else:
            return self.__client.embeds.economy.error_not_enough_money()

    async def withdraw(self, user: disnake.Member, amount: str) -> disnake.Embed:
        """
        Withdraw money from user's bank
        :param user: user to withdraw money from
        :param amount: amount to withdraw

        :return: disnake.Embed
        """
        user = await self.__client.db.users.get(user.id)

        if amount.isnumeric() and int(amount):
            amount = int(amount)
        elif amount in ["max", "all", "სულ"]:
            amount = user.bank
        else:
            return self.__client.embeds.economy.error_invalid_amount_entered()

        if user.bank >= amount:
            user.bank -= amount
            user.wallet += amount
            await self.__client.db.users.update(user)
            return self.__client.embeds.economy.success_withdraw(user, amount)

        else:
            return self.__client.embeds.economy.error_not_enough_money()

    async def give(self,
                   inter: disnake.ApplicationCommandInteraction,
                   sender: disnake.Member,
                   receiver: disnake.Member,
                   amount: str) -> None:
        """
        Give money to another user
        :param inter: command interaction
        :param sender: user who gives money
        :param receiver: user who receives money
        :param amount: amount to give

        :return: None
        """
        if sender == receiver:
            await inter.send(embed=self.__client.embeds.economy.error_self_give())

        this  = await self.__client.db.users.get(sender.id)
        other = await self.__client.db.users.get(receiver.id)

        if sender is None or receiver is None:
            await inter.send(embed=self.__client.embeds.economy.error_user_not_found(other.username))

        if amount.isnumeric() and int(amount):
            amount = int(amount)
        elif amount in ["max", "all", "სულ"]:
            amount = this.wallet
        else:
            await inter.send(embed=self.__client.embeds.economy.error_invalid_amount_entered())

        if amount == 0:
            await inter.send(embed=self.__client.embeds.economy.error_zero_give())

        if this.wallet + this.bank < amount:
            await inter.send(embed=self.__client.embeds.economy.error_not_enough_money(
                where=f"რათა მიცე {other.username}'ს {amount} ფული",
            ))

        if amount >= 100:
            em = self.__client.embeds.utils.confirmation_needed(f"{other.name}-ისთვის {amount} ₾-ის მიცემა?")
            confirmation = self.__client.buttons.YesNoButton(intended_user=sender)
            await inter.send(embed=em, view=confirmation)
            await confirmation.wait()

            if not confirmation.choice:
                em = self.__client.embeds.utils.cancelled(f"შენ გადაიფიქრე {receiver.name}'ისთვის {amount} ის მიცემა")
                await inter.edit_original_message(embed=em, view=None)
                return

        if this.wallet >= amount:
            this.wallet -= amount
            other.wallet += amount

        elif this.wallet + this.bank >= amount:
            amount       -= this.wallet
            other.wallet += this.wallet
            this.wallet   = 0
            this.bank    -= amount
            other.wallet += amount

        await self.__client.db.users.update(this)
        await self.__client.db.users.update(other)

        em = self.__client.embeds.economy.success_give(this, other, amount)

        if amount >= 100:
            await inter.edit_original_message(embed=em, view=None)
        else:
            await inter.send(embed=em)

    