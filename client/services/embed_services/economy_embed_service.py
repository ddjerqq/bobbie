import disnake

from database.models.user import User


class EconomyEmbedService:
    def __init__(self, client):
        self.__client = client

    def error_invalid_amount_entered(self) -> disnake.Embed:
        em = disnake.Embed(description=f"შეიყვანე რაოდენობა როგორც რიცხვი, \n"
                                       f"ან დაწერე [max, all, სულ]",
                           color=0x692b2b)
        return em

    async def error_not_enough_money(self, where: str = "") -> disnake.Embed:
        """
        შენ არ გაქვს საკმარისი ფული {where}
        """
        em = disnake.Embed(color=0x692b2b,
                           description=f"შენ არ გაქვს საკმარისი ფული {where}")
        return em

    def error_self_give(self) -> disnake.Embed:
        """
        რაც ცდილობ ბრატ? შენ თავს ვერ მისცემ ფულს!
        """
        em = disnake.Embed(color=0x692b2b,
                           description="რაც ცდილობ ბრატ? შენ თავს ვერ მისცემ ფულს!")
        return em

    def error_zero_give(self) -> disnake.Embed:
        """
        შენ ვერ გასცემ 0 ₾არს
        """
        em = disnake.Embed(color=0x692b2b,
                           description="შენ ვერ გასცემ 0 ₾არს")
        return em

    def error_user_not_found(self, username: str) -> disnake.Embed:
        """
        მომხმარებელი სახელით '{username}' ვერ მოიძებნა!
        """
        em = disnake.Embed(color=0x692b2b,
                           description=f"მომხმარებელი სახელით '{username}' ვერ მოიძებნა!")
        return em

    async def balance(self, target: disnake.Member) -> disnake.Embed:
        """
        get the balance of a user
        """
        user = await self.__client.db.users.get(target.id)

        em = disnake.Embed(
            title=f"{target.name}'ს ბალანსი")

        em.set_thumbnail(url="https://i.imgur.com/7mN9tDJ.png")

        em.add_field(name="ბანკი:",
                     value=f" {user.bank}₾")

        em.add_field(name="საფულე:",
                     value=f" {user.wallet}₾", inline=False)

        em.set_footer(icon_url=target.avatar.url, text=f"Exp: {user.experience}")

        return em

    async def leaderboards(self) -> disnake.Embed:
        """
        get the top10 users by wallet + bank
        """
        em = disnake.Embed(title="ლიდერბორდი", color=0x00ff00)
        users = await self.__client.db.users.get_all()
        top_ten = sorted(users, key=lambda u: u.wallet + u.bank, reverse=True)[:10]

        for idx, user in enumerate(top_ten):
            em.add_field(name=f"[{idx + 1:02}] {user.username}", value=f"net: {user.wallet + user.bank}", inline=False)

        return em

    def success_deposit(self, user: User, amount) -> disnake.Embed:
        """
        წარმატებით შეიტანე ბანკში {amount} ₾
        """
        em = disnake.Embed(description=f"წარმატებით შეიტანე ბანკში {amount} ₾",
                           color=0x2b693a)
        em.add_field(name="ბანკი", value=f"{user.bank}")
        em.add_field(name="საფულე", value=f"{user.wallet}")

        return em

    def success_withdraw(self, user: User, amount: int) -> disnake.Embed:
        """
        წარმატებით გამოიტანე {amount} ₾ ბანკიდან
        """
        em = disnake.Embed(description=f"წარმატებით გამოიტანე {amount} ₾ ბანკიდან",
                           color=0x2b693a)
        em.add_field(name="ბანკი", value=f"{user.bank}")
        em.add_field(name="საფულე", value=f"{user.wallet}")
        return em

    def success_give(self, user: User, target: User, amount: int):
        """
        წარმატებით მიეცი {amount} ₾ მომხმარებელს {target.username}
        """
        em = disnake.Embed(color=0x2b693a,
                           description=f"წარმატებით მიეცი {target.username}'ს {amount}₾")

        em.add_field(name="შები ბანკი",
                     value=f"{user.bank}")
        em.add_field(name="შენი საფულე",
                     value=f"{user.wallet}")
        em.add_field(name="შენი XP",
                     value=f"{user.experience}")

        em.add_field(name=f"{target.username}'ს ბანკი",
                     value=f"{target.bank}")
        em.add_field(name=f"{target.username}'ს საფულე",
                     value=f"{target.wallet}")
        em.add_field(name=f"{target.username}'ს XP",
                     value=f"{target.experience}")
        return em
