import disnake

from database.enums import *
from database.factories.item_factory import ItemFactory
from database.models.item import Item
from database.models.user import User


class InventoryEmbedService:
    def __init__(self, client):
        self.__client = client

    def error_item_not_in_shop(self, item_slug: str) -> disnake.Embed:
        """
        item slug name არ იყიდება
        """
        em = disnake.Embed(description=f"{ItemName[item_slug.upper()]} არ იყიდება",
                           color=0x692b2b)
        return em

    def error_item_not_buyable(self, item_slug: str) -> disnake.Embed:
        """
        შევ ვერ იყიდი {item_slug}ს, მხოლოდ გაყიდვაა შესაძლებელი
        """
        em = disnake.Embed(color=0x692b2b,
                           description=f"შენ ვერ იყიდი {ItemName[item_slug.upper()]}ს, მხოლოდ გაყიდვაა შესაძლებელი")
        return em

    def error_item_not_in_inventory(self, item_slug: str) -> disnake.Embed:
        """
        შენ არ გაქვს {item.name}
        """
        em = disnake.Embed(description=f"შენ არ გაქვს {ItemName[item_slug.upper()].value}",
                           colour=0x692b2b)
        return em

    def error_not_enough_items(self, item_slug: str, amount_needs: int, amount_has: int) -> disnake.Embed:
        """
        შენ არ გაქვს {amount_needs} {item.name}
        შენ გაქვს - {amount_has}
        """
        em = disnake.Embed(color=0x692b2b,
                           description=f"შენ არ გაქვს {amount_needs} {ItemName[item_slug.upper()]},\n"
                                       f"შენ გაქვს - {amount_has}")
        return em

    def success_sold_item(self, item_slug: str, amount: int, total_price: int) -> disnake.Embed:
        """
        შენ გაყიდე {amount} ცალი {item.name}{item.emoji} \n
        ღირებულება: `{total_price}`₾
        """
        item = ItemFactory.new(ItemType[item_slug.upper()])
        em = disnake.Embed(color=0x2b693a,
                           description=f"შენ გაყიდე {amount} ცალი {item.name}{item.emoji}\n"
                                       f"ღირებულება: `{total_price}`₾")
        em.add_field(name="იშვიათობა", value=f"`{item.rarity.value:.4f} - {item.rarity.name}`")
        em.set_thumbnail(item.thumbnail or None)
        em.set_footer(text=f"ID: {item.id}")
        return em

    def success_sold_all_sellables(self, amount: int, total_price: int) -> disnake.Embed:
        """
        შენ გაყიდე {amount} ნივთი \n
        შემოსავალი: `{total_price}`
        """
        em = disnake.Embed(color=0x2b693a,
                           description=f"**შენ გაყიდე {amount} ნივთი**\n"
                                       f"შემოსავალი: `{total_price}`₾")
        em.set_footer(text="(არ დაგავიწყდეს ფულის ბანკში შეტანა, ბევრი ქურდი დახეტიალობს გარეთ)")
        return em

    def success_bought_item(self, item: Item) -> disnake.Embed:
        """
        შენ წარმატებით იყიდე {item.name}{item.emoji}
        """
        em = disnake.Embed(description=f"შენ წარმატებით იყიდე {item.name}{item.emoji}",
                           color=0x2b693a)
        em.add_field(name="იშვიათობა",
                     value=f"`{item.rarity.name}` - `{item.rarity.value:.8f}`")
        em.set_footer(text=f"ID: {item.id}")
        return em

    async def util_inventory(self, target: disnake.Member) -> disnake.Embed:
        # feature remake this
        user = await self.__client.db.users.get(target.id)  # type: User
        total_price = sum(item.price for item in user.items)

        em = disnake.Embed(title=f"{user.username}'ის ინვენტარი",
                           description=f"{len(user.items)} ნივთი, სულ `{total_price}`₾", )

        item_types = {item.type: [] for item in user.items}  # type: dict[ItemType, list[Item]]

        for item in user.items:
            item_types[item.type].append(item)

        for item_type, items in item_types.items():
            tot_price = sum(i.price for i in items)
            total     = len(item_types[item_type])
            em.add_field(name=f"{items[0].emoji} {items[0].name} ─ {total}",
                         value=f"ფასი ჯამში: `{tot_price}`₾")

        # TODO maybe make this prettier later
        # TODO pagination maybe

        return em
