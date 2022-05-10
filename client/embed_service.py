import disnake

from database.models.item import Item
from database.models.user import User
from database.database import Database


class EmbedService:
    def __init__(self, database: Database):
        self._database = database

    @staticmethod
    def message_delete(message: disnake.Message) -> disnake.Embed:
        em = disnake.Embed(title=f"{message.author.name}\nID: {message.author.id}",
                           color=0x2d56a9,
                           timestamp=disnake.utils.utcnow())

        em.set_thumbnail(url=message.author.avatar.url)
        em.add_field(name="ჩანელი", value=message.channel.mention, inline=False)

        if message.attachments:
            em.add_field(
                name="ათაჩმენტ(ებ)ი",
                value="\n".join(map(lambda a: a.url, message.attachments)))

        if message.content:
            em.add_field(
                name="მესიჯი",
                value=message.content, inline=False)

        return em

    async def member_leave(self, member: disnake.Member) -> disnake.Embed:
        em = disnake.Embed(color=0x2d56a9)
        em.add_field(name="სახელი", value=member.name)
        em.add_field(name="შემოვიდა", value=member.joined_at)
        em.set_thumbnail(url=member.avatar.url)
        em.set_footer(text=f"ID: {member.id}")

        # user = await self._database.users.get(member.id)
        # if user is not None:
        #     em.add_field(name="exp", value=user.experience)
        #     em.add_field(name="bank", value=user.bank)
        #     em.add_field(name="wallet", value=user.wallet)
        #     await self._database.users.delete(user)
        return em

    @staticmethod
    def confirmation_needed(action: str) -> disnake.Embed:
        """
        გსურთ {action}?
        ----------------
        | კი |    | არა |
        ----------------
        """
        em = disnake.Embed(color=0xadb04c,
                           description=f"გსურს {action}?")
        return em

    @staticmethod
    def cancelled(text: str = "ტრანზაქცია გაუქმდა") -> disnake.Embed:
        em = disnake.Embed(color=0x692b2b,
                           description=text)
        return em

    @staticmethod
    def cooldown(action: str, reason: str, retry_after: float | int) -> disnake.Embed:
        """
        :param action: შენ უკვე {action}
        :param reason: შენ ისევ შეძლებ {reason}
        :param retry_after: seconds, _error.retry_after
        """
        em = disnake.Embed(color=0x692b2b,
                           description=f"*შენ უკვე {action}*, \n"
                                       f"შენ ისევ შეძლებ {reason} {(retry_after // 60):.0f} წუთში")
        return em

    @staticmethod
    def generic_success(*, title: str = "წარმატება!", description: str = None) -> disnake.Embed:
        em = disnake.Embed(color=0x2b693a, title=title, description=description)
        return em

    @staticmethod
    def generic_error(reason: str) -> disnake.Embed:
        em = disnake.Embed(description=reason,
                           color=0x692b2b)
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
                           color=0x692b2b)
        em.description += f"\nშენ გჭირდება {needs}₾"
        return em

    @staticmethod
    def econ_err_self_give():
        em = disnake.Embed(color=0x692b2b,
                           description="რაც ცდილობ ბრატ? შენ თავს ვერ მისცემ ფულს!")
        return em

    @staticmethod
    def econ_err_zero_give():
        em = disnake.Embed(color=0x692b2b,
                           description="შენ ვერ გასცემ 0 ₾არს")
        return em

    @staticmethod
    def econ_err_user_not_found(username: str) -> disnake.Embed:
        em = disnake.Embed(color=0x692b2b,
                           description=f"მომხმარებელი სახელით '{username}' ვერ მოიძებნა!")
        return em

    async def econ_util_balance(self, target: disnake.Member, /, *, show_bank=False) -> disnake.Embed:
        user = await self._database.users.get(target.id)

        em = disnake.Embed(
            title=f"{target.name}'ს ბალანსი")
        em.set_thumbnail(url="https://i.imgur.com/7mN9tDJ.png")
        if show_bank:
            em.add_field(name="ბანკი:",
                         value=f" {user.bank}₾")
        em.add_field(name="საფულე:",
                     value=f" {user.wallet}₾", inline=False)
        em.set_footer(icon_url=target.avatar.url, text=f"Exp: {user.experience}")

        return em

    async def econ_util_leaderboards(self) -> disnake.Embed:
        em = disnake.Embed(title="ლიდერბორდი", color=0x00ff00)
        users = await self._database.users.get_all()
        top_ten = sorted(users, key=lambda u: u.wallet + u.bank, reverse=True)[:10]
        for idx, user in enumerate(top_ten):
            em.add_field(name=f"[{idx + 1:02}] {user.username}", value=f"net: {user.wallet + user.bank}", inline=False)
        return em

    @staticmethod
    def err_invalid_amount() -> disnake.Embed:
        em = disnake.Embed(description=f"შეიყვანე რაოდენობა როგორც რიცხვი, \n"
                                       f"ან დაწერე [max, all, სულ]",
                           color=0x692b2b)
        return em

    @staticmethod
    def econ_success_deposit(user: User, amount) -> disnake.Embed:
        em = disnake.Embed(description=f"წარმატებით შეიტანე ბანკში {amount} ₾",
                           color=0x2b693a)
        em.add_field(name="ბანკი", value=f"{user.bank}")
        em.add_field(name="საფულე", value=f"{user.wallet}")
        return em

    @staticmethod
    def econ_success_withdraw(user: User, amount: int) -> disnake.Embed:
        em = disnake.Embed(description=f"წარმატებით გამოიტანე {amount} ₾ ბანკიდან",
                           color=0x2b693a)
        em.add_field(name="ბანკი", value=f"{user.bank}")
        em.add_field(name="საფულე", value=f"{user.wallet}")
        return em

    @staticmethod
    def econ_success_give(user: User, target: User, amount: int):
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

    @staticmethod
    def inv_err_item_not_in_shop(item_slug: str) -> disnake.Embed:
        item = Item.new(item_slug)
        em = disnake.Embed(description=f"{item.name} არ იყიდება",
                           color=0x692b2b)
        return em

    @staticmethod
    def inv_err_item_not_buyable(item_slug: str) -> disnake.Embed:
        item = Item.new(item_slug)
        em = disnake.Embed(color=0x692b2b,
                           description=f"შენ ვერ იყიდი {item.name}ს, მხოლოდ გაყიდვაა შესაძლებელი")
        return em

    @staticmethod
    def inv_err_item_not_in_inventory(item: str) -> disnake.Embed:
        item = Item.new(item)
        em = disnake.Embed(description=f"შენ არ გაქვს {item.name}",
                           colour=0x692b2b)
        return em

    @staticmethod
    def inv_err_not_enough_items(item_type: str, amount_needs: int, amount_has: int) -> disnake.Embed:
        """
        შენ არ გაქვს {amount_needs} {item.name}
        შენ გაქვს - {amount_has}
        """
        item = Item.new(item_type)
        em = disnake.Embed(color=0x692b2b,
                           description=f"შენ არ გაქვს {amount_needs} {item.name},\n"
                                       f"შენ გაქვს - {amount_has}")
        return em

    @staticmethod
    def inv_success_sold_item(item_type: str, amount: int, total_price: int) -> disnake.Embed:
        item = Item.new(item_type)
        em = disnake.Embed(color=0x2b693a,
                           description=f"შენ გაყიდე {amount} ცალი {item.name}{item.emoji}\n"
                                       f"ღირებულება: `{total_price}`₾")
        em.add_field(name="იშვიათობა", value=f"`{item.rarity:.4f} - {item.rarity_string}`")
        em.set_thumbnail(item.thumbnail or None)
        em.set_footer(text=f"ID: {item.id}")
        return em

    @staticmethod
    def inv_success_sold_all_sellables(amount: int, total_price: int) -> disnake.Embed:
        em = disnake.Embed(color=0x2b693a,
                           description=f"**შენ გაყიდე {amount} ნივთი**\n"
                                       f"შემოსავალი: `{total_price}`₾")
        em.set_footer(text="(არ დაგავიწყდეს ფულის ბანკში შეტანა, ბევრი ქურდი დახეტიალობს გარეთ)")
        return em

    @staticmethod
    def inv_success_bought_item(item: Item) -> disnake.Embed:
        em = disnake.Embed(description=f"შენ წარმატებით იყიდე {item.name}{item.emoji}",
                           color=0x2b693a)
        em.add_field(name="იშვიათობა",
                     value=f"`{item.rarity_string}` - `{item.rarity:.8f}`")
        # em.set_footer(text=f"ID: {item.id}")
        return em

    async def inv_util_inventory(self, target: disnake.Member) -> disnake.Embed:
        user = await self._database.users.get(target.id)
        items = user.items

        total_price = sum(item.price for item in items)

        em = disnake.Embed(title=f"{user.username}'ის ინვენტარი",
                           description=f"{len(items)} ნივთი, სულ `{total_price}`₾", )

        item_types: dict[str, list[Item]] = {i: [] for i in set(map(lambda x: x.type, items))}

        for item in items:
            item_types[item.type].append(item)

        for item_type, items in item_types.items():
            item_types[item_type].sort(key=lambda x: x.rarity)
            tot_price = sum(i.price for i in items)
            tot = len(item_types[item_type])
            em.add_field(name=f"{items[0].emoji} {items[0].name} ─ {tot}",
                         value=f"ფასი ჯამში: `{tot_price}`₾")

        return em

    @staticmethod
    def fish(item: Item, broken: bool) -> disnake.Embed:
        tool = Item.new("fishing_rod")
        em = disnake.Embed(description=f"შენ წახვედი სათევზაოდ და დაიჭირე **{item.name}** {tool.emoji}",
                           color=0x2b693a if not broken else 0x692b2b)
        em.description += f"\n**შენ გატეხე შენი ანკესი! არ დაგავიწყდეს ახლის ყიდვა მაღაზიაში!**" if broken else ""
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
        em = disnake.Embed(description=f"შენ წახვედი სანადიროდ და მოინადირე **{item.name}** {tool.emoji}",
                           color=0x2b693a if not broken else 0x692b2b)
        em.description += "\n**შენ გატეხე შენი სანადირო თოფი! არ დაგავიწყდეს ახლის ყიდვა მაღაზიაში!**" if broken else ""
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
                                       f"**{item.name}** {tool.emoji}",
                           color=0x2b693a if not broken else 0x692b2b)
        em.description += "\n**შენ გატეხე შენი ნიჩაბი! არ დაგავიწყდეს ახლის ყიდვა მაღაზიაში!**" if broken else ""
        em.add_field(name="ღირებულება",
                     value=f"`{item.price}` ₾")
        em.add_field(name="იშვიათობა",
                     value=f"`{item.rarity_string}`\n")
        em.add_field(name="იშვიათობა",
                     value=f"`{item.rarity:.8f}`")
        em.set_thumbnail(url=item.thumbnail or tool.thumbnail)
        return em


    @staticmethod
    def wordle_grid(grid: list[list[int]],
                    /,
                    *,
                    has: set[str] = None,
                    hasnt: set[str] = None,
                    index: dict[int, str] = None,
                    author: disnake.Member = None) -> disnake.Embed:
        grid_emoji = {
            -1: "🔳",
            0: "⬛",
            1: "🟨",
            2: "🟩",
        }

        em = disnake.Embed(color=0x0f0f0f, title=f"GeoWordle {author.name}")
        desc = ""

        for row in grid:
            for cell in row:
                desc += grid_emoji[cell]
            desc += "\n"

        em.description = desc + "\n"

        if has:
            em.add_field(name="სიტყვას აქვს:",
                         value='`' + ', '.join(has) + '`',
                         inline=False)
        if hasnt:
            em.add_field(name="სიტყვას არ აქვს:",
                         value='`' + ', '.join(hasnt) + '`',
                         inline=False)
        if index:
            footer = ["_", "_", "_", "_", "_"]
            for idx, char in index.items():
                footer[idx] = char

            em.add_field(name="სიტყვა: ",
                         value='`' + " ".join(footer) + '`',
                         inline=False)

        return em
