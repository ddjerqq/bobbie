import random

import disnake
from client.client import Client
from database import ItemType
from database.factories.item_factory import ItemFactory


class JobService:
    def __init__(self, client: Client):
        self.__client = client


    async def rob(self, robber: disnake.Member, target: disnake.Member) -> disnake.Embed:
        """
        Rob target
        :param robber: robber
        :param target: target
        :return: disnake.Embed
        """
        this  = await self.__client.db.users.get(robber.id)
        other = await self.__client.db.users.get(target.id)
        items = this.items

        if this == other:
            return self.__client.embeds.generic.generic_error("შენ ვერ გაძარცვავ შენს თავს")

        elif other.wallet < 10:
            return self.__client.embeds.generic_error(
                f"შენ ვერ გაძარცვავ {target.name}'ს, რადგან მას ჯიბეში კაპეიკი არ უდევს"
            )

        elif ItemType.KNIFE in [i.type for i in items]:

            if random.random() < 0.1:
                other.wallet += this.wallet
                this.wallet = 0

                await self.__client.db.users.update(this)
                await self.__client.db.users.update(other)

                return self.__client.embeds.generic_success(
                    title=f"შენ მოკვდი {target.name}'ის ძარცვის დროს🤣",
                    description=f"შენი საფულე გადაეცა {target.name}'ს"
                )

            else:
                steal_amount  = random.randint(other.wallet // 4, other.wallet // 2)
                this.wallet  += steal_amount
                other.wallet -= steal_amount
                await self.__client.db.users.update(other)
                await self.__client.db.users.update(this)

                knife = sorted(items, key=lambda i: i.rarity.value, reverse=True)[0]

                _, broken = ItemFactory.use(knife)

                em = self.__client.embeds.generic.generic_success(
                    description=f"**შენ გაძარცვე** {target.mention}\nმას მოპარე {steal_amount}₾"
                )
                em.description += f"\nშენ გატეხე შენი დანა {target.name}ის ძარცვის დროს" if broken else ""
                return em

        else:
            return self.__client.embeds.generic.generic_error(
                f"შენ ცადე {target.name}'ს გაძარცვა, მაგრამ დანის გარეშე მან სახეში გაგილაწუნა და გაიქცა"
            )


    async def work(self, worker: disnake.Member) -> disnake.Embed:
        """
        Work
        :param worker: worker
        :return: disnake.Embed
        """
        pay  = self.__client.config.get("economy").get("work_pay")

        user = await self.__client.db.users.get(worker.id)
        user.experience += 1
        user.wallet += pay
        await self.__client.db.users.update(user)

        em = disnake.Embed(
            description=f"**წარმატებული დღე!**\n"
                        f"შენ წახვედი სამსახურში და გამოიმუშავე `{pay}` ₾ <:hammercampfire:960423335437680692>",
            color=0x2b693a)
        em.set_footer(text="(არ დაგავიწყდეს ფულის ბანკში შეტანა, ბევრი ქურდი დახეტიალობს გარეთ)")
        return em
