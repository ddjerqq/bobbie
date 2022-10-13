import disnake

from database import ItemType
from database.factories.item_factory import ItemFactory
from database.models.item import Item


class UtilsEmbedService:
    def __init__(self, client):
        self.__client = client

    def deleted_message(self, message: disnake.Message) -> disnake.Embed:
        """
        {message.author.name} \n
        ID: {message.author.id}

        ---------------------
        timestamp
        """
        em = disnake.Embed(title=f"{message.author.name}\n"
                                 f"ID: {message.author.id}",
                           color=0x2d56a9,
                           timestamp=disnake.utils.utcnow())
        em.set_thumbnail(url=message.author.avatar.url)
        em.add_field(name="ჩანელი", value=message.channel.mention, inline=False)

        if message.attachments:
            em.add_field(name="ათაჩმენტ(ებ)ი",
                         value="\n".join(map(lambda a: a.url, message.attachments)))

        if message.content:
            em.add_field(name="მესიჯი",
                         value=message.content, inline=False)

        return em

    async def member_leave(self, member: disnake.Member) -> disnake.Embed:
        """
        სახელი:   member.name
        შემოვიდა: member.joined_at
        """
        em = disnake.Embed(color=0x2d56a9)
        em.add_field(name="სახელი", value="N/A" if not member else member.name)
        em.add_field(name="შემოვიდა", value="N/A" if not member else member.joined_at)
        em.set_thumbnail(url="N/A" if not member else member.avatar.url)
        em.set_footer(text="N/A" if not member else f"ID: {member.id}")

        return em

    def confirmation_needed(self, action: str) -> disnake.Embed:
        """
        გსურს {action}?
        ----------------
        | კი |    | არა |
        ----------------
        """
        em = disnake.Embed(color=0xadb04c,
                           description=f"გსურს {action}?")
        return em

    def cancelled(self, text: str = "ტრანზაქცია გაუქმდა") -> disnake.Embed:
        """
        ტრანზაქცია გაუქმდა
        """
        em = disnake.Embed(color=0x692b2b,
                           description=text)
        return em

    def cooldown(self, action: str, reason: str, retry_after: float | int) -> disnake.Embed:
        """
        შენ უკვე {action}
        შენ ისევ შეძლებ {reason}
        """
        em = disnake.Embed(color=0x692b2b,
                           description=f"*შენ უკვე {action}*, \n"
                                       f"შენ ისევ შეძლებ {reason} {(retry_after // 60):.0f} წუთში")
        return em

    def fish(self, item: Item, broken: bool) -> disnake.Embed:
        """
        fish,
        broken: bool
        """
        tool = ItemFactory.new(ItemType.FISHING_ROD)
        em = disnake.Embed(description=f"შენ წახვედი სათევზაოდ და დაიჭირე **{item.name}** {tool.emoji}",
                           color=0x2b693a if not broken else 0x692b2b)
        em.description += f"\n***შენ გატეხე შენი ანკესი! არ დაგავიწყდეს ახლის ყიდვა მაღაზიაში!***" if broken else ""

        em.add_field(name="ღირებულება",
                     value=f"`{item.price}` ₾")

        em.add_field(name="იშვიათობა",
                     value=f"`{item.rarity.name}`\n")

        em.add_field(name="იშვიათობა",
                     value=f"`{item.rarity.value:.8f}`")
        em.set_thumbnail(url=item.thumbnail or tool.thumbnail)
        return em

    def hunt(self, item: Item, broken: bool) -> disnake.Embed:
        tool = ItemFactory.new(ItemType.HUNTING_RIFLE)

        em = disnake.Embed(description=f"შენ წახვედი სანადიროდ და მოინადირე **{item.name}** {tool.emoji}",
                           color=0x2b693a if not broken else 0x692b2b)

        em.description += "\n**შენ გატეხე შენი სანადირო თოფი! არ დაგავიწყდეს ახლის ყიდვა მაღაზიაში!**" if broken else ""

        em.add_field(name="ღირებულება",
                     value=f"`{item.price}` ₾")

        em.add_field(name="იშვიათობა",
                     value=f"`{item.rarity.name}`\n")

        em.add_field(name="იშვიათობა",
                     value=f"`{item.rarity.value:.8f}`")

        em.set_thumbnail(url=item.thumbnail or tool.thumbnail)
        return em

    def dig(self, item: Item, broken: bool) -> disnake.Embed:
        tool = ItemFactory.new(ItemType.SHOVEL)

        em = disnake.Embed(description=f"შენ გადაწყვიტე ამოგეთხრა სადმე მიწა, ბევრი ოფლის დაღვრის მერე შენ იპოვე "
                                       f"**{item.name}** {tool.emoji}",
                           color=0x2b693a if not broken else 0x692b2b)

        em.description += "\n**შენ გატეხე შენი ნიჩაბი! არ დაგავიწყდეს ახლის ყიდვა მაღაზიაში!**" if broken else ""

        em.add_field(name="ღირებულება",
                     value=f"`{item.price}` ₾")

        em.add_field(name="იშვიათობა",
                     value=f"`{item.rarity.name}`\n")

        em.add_field(name="იშვიათობა",
                     value=f"`{item.rarity.value:.8f}`")

        em.set_thumbnail(url=item.thumbnail or tool.thumbnail)
        return em
