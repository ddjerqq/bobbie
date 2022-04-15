from datetime import datetime
import disnake

from models.item import Item, ITEMS_AND_PRICES, EMOJIS
from models.user import User
from models.database import Database


class EmbedService:
    def __init__(self, database: Database):
        self._database = database

    def cooldown(self, action: str, reason: str, retry_after: float | int) -> disnake.Embed:
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

    def rob_success(self, target: disnake.Member, stolen: int) -> disnake.Embed:
        em = disnake.Embed(color=0x00ff00,
                           description=f"წარმატებით გაძარცვე {target.name}")
        em.description += f"\nმოპარე {stolen} ₾"
        return em

    def rob_success_died(self, target: disnake.Member) -> disnake.Embed:
        em = disnake.Embed(color=0xff0000, title=f"შენ მოკვდი {target.name}'ის ძარცვის დროს 🤣",
                           description=f"შენი საფულე გადაეცა {target.name}'ს")
        return em

    def rob_err(self, reason: str) -> disnake.Embed:
        em = disnake.Embed(description=reason,
                           color=0xff0000)
        return em

    def econ_err_not_enough_money(self, where: str = "", _for: str = "", needs: int = "") -> disnake.Embed:
        """
        :param where: wallet or bank
        :param _for: what you are trying to buy
        :param needs: how much money the user needs
        """
        em = disnake.Embed(description=f"შენ არ გაქვს საკმარისი ფული {where} {_for}",
                           color=0xff0000)
        em.description += f"\nშენ გჭირდება {needs} ₾"
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

    def econ_err_invalid_amount(self) -> disnake.Embed:
        em = disnake.Embed(description=f"შეიყვანე რაოდენობა როგორც რიცხვი, \n"
                                       f"ან დაწერე [max, all, სულ]",
                           color=0xff0000)
        return em

    def econ_success_deposit(self, user: User, amount) -> disnake.Embed:
        em = disnake.Embed(description=f"წარმატებით შეიტანე ბანკში {amount} ₾",
                           color=0x00ff00)
        em.add_field(name="ბანკი", value=f"{user.bank}")
        em.add_field(name="საფულე", value=f"{user.wallet}")
        return em

    def econ_success_withdraw(self, user: User, amount: int) -> disnake.Embed:
        em = disnake.Embed(description=f"წარმატებით გამოიტანე {amount} ₾ ბანკიდან",
                           color=0x00ff00)
        em.add_field(name="ბანკი", value=f"{user.bank}")
        em.add_field(name="საფულე", value=f"{user.wallet}")
        return em

    def inv_err_item_not_in_shop(self, item_slug: str) -> disnake.Embed:
        em = disnake.Embed(description=f"{item_slug} არ არსებობს",
                           color=0xff0000)
        return em

    def inv_err_item_not_buyable(self, item_slug: str) -> disnake.Embed:
        em = disnake.Embed(color=0xff0000,
                           description=f"შენ ვერ იყიდი {item_slug}ს, მხოლოდ გაყიდვაა შესაძლებელი")
        return em

    def inv_err_item_not_in_inventory(self, item: str):
        em = disnake.Embed(description=f"შენ არ გაქვს {item}",
                           colour=0xff0000)
        return em

    def inv_success_bought_item(self, item: Item) -> disnake.Embed:
        em = disnake.Embed(description=f"წარმაბით იყიდე {item.type}",
                           color=0x00ff00)

        em.add_field(name="იშვიათობა",
                     value=f"`{item.rarity_string}` - `{item.rarity:.8f}`")

        em.set_footer(text=f"Item ID: {item.id}")
        return em

    async def inv_util_inventory(self, target: disnake.Member) -> disnake.Embed:
        user = await self._database.user_service.get(target.id)
        items = await self._database.item_service.get_all_by_owner_id(user.id)

        total_price = sum(item.price for item in items)

        em = disnake.Embed(title=f"{user.username}'ის ინვენტარი",
                           description=f"{len(items)} ნივთი, სულ {total_price} ₾",
                           color=0x00ff00)

        item_types: dict[str, list[Item]] = {i: [] for i in set(map(lambda x: x.type, items))}

        for item in items:
            item_types[item.type].append(item)

        for item_type, items in item_types.items():
            item_types[item_type].sort(key=lambda x: x.rarity)
            top = item_types[item_type][0]
            avg_rarity = sum(i.rarity for i in items) / len(items)
            avg_price  = sum(i.price for i in items) // len(items)

            em.add_field(name=f"{EMOJIS.get(item_type, '')}{item_type}: {len(item_types[item_type])}",
                         value=f"`{top.rarity_string}` - `{top.rarity:.8f}`\n"
                               f"`საშუალო იშვიათობა`: `{avg_rarity:.4f}`\n"
                               f"`საშუალო ფასი`: `{avg_price}` ₾/",
                         inline=False)

        return em

    def fish(self, item: Item, broken: bool) -> disnake.Embed:
        em = disnake.Embed(description=f"შენ წახვდედი სათევზაოდ და დაიჭირე {item.type} {EMOJIS['fishing_rod']}",
                           color=0x00ff00 if not broken else 0xff0000)
        em.description += "\nშენ გატეხე შენი ანკესი" if broken else ""
        em.add_field(name="ღირებულება",
                     value=f"`{item.price}` ₾")
        em.add_field(name="იშვიათობა",
                     value=f"`{item.rarity_string}` - `{item.rarity:.8f}`")
        return em

    def hunt(self, item: Item, broken: bool) -> disnake.Embed:
        em = disnake.Embed(description=f"შენ წახვედი სანადიროდ ტყეში და მოინადირე {item.type} {EMOJIS['hunting_rifle']}",
                           color=0x00ff00 if not broken else 0xff0000)
        em.description += "\nშენ გატეხე შენი სანადირო თოფი" if broken else ""
        em.add_field(name="ღირებულება",
                     value=f"`{item.price}` ₾")
        em.add_field(name="იშვიათობა",
                     value=f"`{item.rarity_string}` - `{item.rarity:.8f}`")
        return em

    def dig(self, item: Item, broken: bool) -> disnake.Embed:
        em = disnake.Embed(description=f"შენ გადაწყვიტე ამოგეთხრა სადმე და იპოვე {item.type} {EMOJIS['shovel']}",
                           color=0x00ff00 if not broken else 0xff0000)
        em.description += "\nშენ გატეხე შენი ნიჩაბი" if broken else ""
        em.add_field(name="ღირებულება",
                     value=f"`{item.price}` ₾")
        em.add_field(name="იშვიათობა",
                     value=f"`{item.rarity_string}` - `{item.rarity:.8f}`")
        return em

    def sell(self, item: Item) -> disnake.Embed:
        em = disnake.Embed(description=f"შენ წახვედი მარკეტში და გაყიდე შენი {item.type}",
                           color=0x00ff00)
        em.add_field(name="ღირებულება",
                     value=f"`{item.price}` ₾")
        em.add_field(name="იშვიათობა",
                     value=f"`{item.rarity_string}` - `{item.rarity:.8f}`")
        creation_date = datetime.fromtimestamp(item.creation_date).strftime("%d/%m/%Y %H:%M:%S")
        em.set_footer(text=f"ID: {item.id} | created at: {creation_date}")
        return em
