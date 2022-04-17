import disnake

from models.item import Item
from models.user import User
from models.database import Database


class EmbedService:
    def __init__(self, database: Database):
        self._database = database

    @staticmethod
    def cooldown(action: str, reason: str, retry_after: float | int) -> disnake.Embed:
        """
        :param action: შენ უკვე {action}
        :param reason: შენ ისევ შეძლებ {reason}
        :param retry_after: seconds, _error.retry_after
        """
        embed = disnake.Embed(title=f"ნელა ზვიადი",
                              color=0xFF0000,
                              description=f"შენ უკვე {action}, \n"
                                          f"შენ ისევ შეძლებ {reason} {(retry_after // 60):.0f} წუთში")
        return embed

    @staticmethod
    def rob_success(target: disnake.Member, stolen: int) -> disnake.Embed:
        em = disnake.Embed(color=0x00ff00,
                           description=f"წარმატებით გაძარცვე {target.name}")
        em.description += f"\nმოპარე {stolen} ₾"
        return em

    @staticmethod
    def rob_success_died(target: disnake.Member) -> disnake.Embed:
        em = disnake.Embed(color=0xff0000, title=f"შენ მოკვდი {target.name}'ის ძარცვის დროს 🤣",
                           description=f"შენი საფულე გადაეცა {target.name}'ს")
        return em

    @staticmethod
    def rob_err(reason: str) -> disnake.Embed:
        em = disnake.Embed(description=reason,
                           color=0xff0000)
        return em

    @staticmethod
    def econ_err_not_enough_money(where: str = "", _for: str = "", needs: int = "") -> disnake.Embed:
        """
        შენ არ გაქვს საკმარისი ფული {where} {_for} \n
        შენ გჭირდება {needs} ₾ \n
        :param where: wallet or bank
        :param _for: what you are trying to buy
        :param needs: how much money the user needs
        """
        em = disnake.Embed(description=f"შენ არ გაქვს საკმარისი ფული {where} {_for}",
                           color=0xff0000)
        em.description += f"\nშენ გჭირდება {needs} ₾"
        return em

    @staticmethod
    def econ_err_self_give():
        em = disnake.Embed(color=0xff0000,
                           description="შენ ვერ მიცემ შენს თავს ფულს")
        return em

    @staticmethod
    def econ_err_user_not_found(username: str) -> disnake.Embed:
        em = disnake.Embed(color=0xff0000,
                           description=f"მომხმარებელი სახელით '{username}' არ არის ბაზაში")
        return em

    async def econ_util_balance(self, target: disnake.Member) -> disnake.Embed:
        user = await self._database.user_service.get(target.id)

        em = disnake.Embed(
            title=f"{target.name}'ს ბალანსი",
            color=0x2d56a9)
        em.set_thumbnail(url=target.avatar.url)

        em.add_field(name="ბანკი",
                     value=f"{user.bank}")
        em.add_field(name="საფულე",
                     value=f"{user.wallet}")
        em.set_footer(text=f"Exp: {user.experience}")

        return em

    @staticmethod
    def econ_err_invalid_amount() -> disnake.Embed:
        em = disnake.Embed(description=f"შეიყვანე რაოდენობა როგორც რიცხვი, \n"
                                       f"ან დაწერე [max, all, სულ]",
                           color=0xff0000)
        return em

    @staticmethod
    def econ_success_deposit(user: User, amount) -> disnake.Embed:
        em = disnake.Embed(description=f"წარმატებით შეიტანე ბანკში {amount} ₾",
                           color=0x00ff00)
        em.add_field(name="ბანკი", value=f"{user.bank}")
        em.add_field(name="საფულე", value=f"{user.wallet}")
        return em

    @staticmethod
    def econ_success_withdraw(user: User, amount: int) -> disnake.Embed:
        em = disnake.Embed(description=f"წარმატებით გამოიტანე {amount} ₾ ბანკიდან",
                           color=0x00ff00)
        em.add_field(name="ბანკი", value=f"{user.bank}")
        em.add_field(name="საფულე", value=f"{user.wallet}")
        return em

    @staticmethod
    def econ_success_give(user: User, target: User, amount: int):
        em = disnake.Embed(color=0x00ff00,
                           description=f"წარმატებით მიეცი {target.username}'ს {amount} ₾")

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

    @staticmethod
    def inv_err_item_not_in_shop(item_slug: str) -> disnake.Embed:
        item = Item.new(item_slug)
        em = disnake.Embed(description=f"{item.name} არ იყიდება",
                           color=0xff0000)
        return em

    @staticmethod
    def inv_err_item_not_buyable(item_slug: str) -> disnake.Embed:
        item = Item.new(item_slug)
        em = disnake.Embed(color=0xff0000,
                           description=f"შენ ვერ იყიდი {item.name}ს, მხოლოდ გაყიდვაა შესაძლებელი")
        return em

    @staticmethod
    def inv_err_item_not_in_inventory(item: str):
        item = Item.new(item)
        em = disnake.Embed(description=f"შენ არ გაქვს {item.name}",
                           colour=0xff0000)
        return em

    @staticmethod
    def inv_success_bought_item(item: Item) -> disnake.Embed:
        em = disnake.Embed(description=f"წარმაბით იყიდე {item.name}",
                           color=0x00ff00)
        em.add_field(name="იშვიათობა",
                     value=f"`{item.rarity_string}` - `{item.rarity:.8f}`")
        em.set_footer(text=f"ID: {item.id}")
        return em

    async def inv_util_inventory(self, target: disnake.Member) -> disnake.Embed:
        user = await self._database.user_service.get(target.id)
        items = await self._database.item_service.get_all_by_owner_id(user.id)

        total_price = sum(item.price for item in items)

        em = disnake.Embed(title=f"{user.username}'ის ინვენტარი",
                           description=f"{len(items)} ნივთი, სულ {total_price} ₾",)

        item_types: dict[str, list[Item]] = {i: [] for i in set(map(lambda x: x.type, items))}

        for item in items:
            item_types[item.type].append(item)

        for item_type, items in item_types.items():
            item_types[item_type].sort(key=lambda x: x.rarity)
            tot_price = sum(i.price for i in items)

            em.add_field(name=f"{items[0].emoji}{items[0].name} ─ {len(item_types[item_type])}",
                         value=f"`ჯამური ფასი`: `{tot_price}` ₾")

        return em

    @staticmethod
    def fish(item: Item, broken: bool) -> disnake.Embed:
        tool = Item.new("fishing_rod")
        em = disnake.Embed(description=f"შენ წახვედი სათევზაოდ და დაიჭირე ***{item.name}*** {tool.emoji}",
                           color=0x00ff00 if not broken else 0xff0000)
        em.description += "\nშენ გატეხე შენი ანკესი" if broken else ""
        em.add_field(name="ღირებულება",
                     value=f"`{item.price}` ₾")
        em.add_field(name="იშვიათობა",
                     value=f"`{item.rarity_string}`\n")
        em.add_field(name="იშვიათობა",
                     value=f"`{item.rarity:.8f}`")
        em.set_thumbnail(url=item.thumbnail or tool.thumbnail)
        return em

    @staticmethod
    def hunt(item: Item, broken: bool) -> disnake.Embed:
        tool = Item.new("hunting_rifle")
        em = disnake.Embed(description=f"შენ წახვედი სანადიროდ და მოინადირე ***{item.name}*** {tool.emoji}",
                           color=0x00ff00 if not broken else 0xff0000)
        em.description += "\nშენ გატეხე შენი სანადირო თოფი" if broken else ""
        em.add_field(name="ღირებულება",
                     value=f"`{item.price}` ₾")
        em.add_field(name="იშვიათობა",
                     value=f"`{item.rarity_string}`\n")
        em.add_field(name="იშვიათობა",
                     value=f"`{item.rarity:.8f}`")
        em.set_thumbnail(url=item.thumbnail or tool.thumbnail)
        return em

    @staticmethod
    def dig(item: Item, broken: bool) -> disnake.Embed:
        tool = Item.new("shovel")
        em = disnake.Embed(description=f"შენ გადაწყვიტე ამოგეთხრა სადმე მიწა, ბევრი ოფლის დაღვრის მერე შენ იპოვე "
                                       f"***{item.name}*** {tool.emoji}",
                           color=0x00ff00 if not broken else 0xff0000)
        em.description += "\nშენ გატეხე შენი ნიჩაბი" if broken else ""
        em.add_field(name="ღირებულება",
                     value=f"`{item.price}` ₾")
        em.add_field(name="იშვიათობა",
                     value=f"`{item.rarity_string}`\n")
        em.add_field(name="იშვიათობა",
                     value=f"`{item.rarity:.8f}`")
        em.set_thumbnail(url=item.thumbnail or tool.thumbnail)
        return em

    @staticmethod
    def sell(item: Item) -> disnake.Embed:
        em = disnake.Embed(description=f"შენ გაყიდე {item.name}{item.emoji}",
                           color=0x00ff00)
        em.add_field(name="ღირებულება",
                     value=f"`{item.price}` ₾")
        em.add_field(name="იშვიათობა",
                     value=f"`{item.rarity_string}` - `{item.rarity:.8f}`")
        em.set_footer(text=f"ID: {item.id} | Created at: {item.creation_date}")
        return em
