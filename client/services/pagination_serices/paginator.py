import itertools

import disnake
import disnake.ui
from disnake import ApplicationCommandInteraction as Inter
from client.services.pagination_serices.paginator_buttons import PaginatorButtons
import typing

from database.models.item import Item
from database.models.user import User

if typing.TYPE_CHECKING:
    from client.client import Client


def groupby(data: typing.Iterable, key=lambda x: x) -> dict:
    result = {key(item): [] for item in data}
    for item in data:
        result[key(item)].append(item)
    return result


class PaginatorService:
    def __init__(self, client: "Client"):
        self.__client = client


    def generate_pages(self, user: User) -> list[disnake.Embed]:
        group = groupby(user.items, lambda x: x.type)
        total_price = sum(map(lambda i: i.price, user.items))

        grouped_items = {type_: list(sorted(items, key=lambda i: i.rarity.value)) for type_, items in group.items()}
        grouped_items = {sk: grouped_items[sk] for sk in sorted(grouped_items, key=lambda x: x.name)}

        pages = [dict(list(grouped_items.items())[i: i + 10]) for i in range(0, len(grouped_items), 10)]

        embeds: list[disnake.Embed] = []
        for idx, page in enumerate(pages):
            em = disnake.Embed(
                title=f"{user.username}'ის ინვენტარი - {idx + 1}/{len(pages)}",
                color=0x00ff00,
            )
            for type_, items in page.items():
                em.add_field(
                    name=f"{items[0].emoji} {items[0].name} {len(items)}",
                    value=f"`{items[0].id}` - `{items[0].rarity.value:.6f}` - `{items[0].price}`₾",
                    inline=False,
                )
            em.set_footer(text=f"სულ ფასი: {total_price}₾ | სულ ნივთი {len(user.items)}")
            embeds.append(em)

        return embeds

    async def inventory_pages(self, inter: Inter):
        user  = await self.__client.db.users.get(inter.author.id)
        pages = self.generate_pages(user)

        btn = PaginatorButtons(
            inter.author,
            timeout=300,
            pages=pages,
        )
        await inter.response.send_message(embed=pages[0], view=btn)
        btn.message = await inter.original_message()
