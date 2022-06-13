import disnake
from disnake import ui, SelectOption, TextInputStyle, ModalInteraction

from client.client import Client
from database import ItemType
from database.factories.item_factory import ItemFactory
from database.id import Id
from database.models.item import Item
from database.rarity import Rarity


class ItemCreateModal(ui.Modal):
    def __init__(self, client: Client):
        item_type_select_options = [
            SelectOption(label=item.type.name, value=item.type.value, description=item.name, emoji="🔰")
            for item in map(lambda t: ItemFactory.new(t), ItemType)
        ]

        components = [
            ui.Select(
                custom_id="type",
                options=item_type_select_options,
            ),
            ui.TextInput(
                label="rarity",
                custom_id="rarity",
                style=TextInputStyle.short,
                placeholder="0.0 - 1.0",
                required=True,
                min_length=3,
                max_length=16,
            ),
            ui.TextInput(
                label="owner's id",
                custom_id="owner_id",
                style=TextInputStyle.short,
                placeholder="0.0 - 1.0",
            ),
        ]


        super().__init__(
            title="create item",
            custom_id="create_item",
            components=components,
            timeout=300,
        )


    async def callback(self, inter: ModalInteraction) -> None:
        print(inter.data)
        print(inter.text_values)

        print(inter.token)


        type     = ItemType[inter.text_values.get("type")]
        rarity   = float(inter.text_values.get("rarity"))
        owner_id = int(inter.text_values.get("owner_id", str(inter.author.id)))

        id     = Id.new()
        rarity = Rarity(rarity)
        item   = Item(id, type, rarity, owner_id)

        em = disnake.Embed(title="Item Created!")

        if item.thumbnail:
            em.set_thumbnail(url=item.thumbnail)

        em.add_field(name="item type", value=item.name)
        em.add_field(name="item rarity", value=f"{item.rarity.value} - {item.rarity.value}")
        em.add_field(name="item price", value=item.price)
        em.set_footer(text=f"ID: {item.id} owner: {item.owner_id}")

        await inter.response.send_message(embed=em)


    async def on_error(self, error: Exception, interaction: ModalInteraction) -> None:
        await interaction.response.send_message(embed=disnake.Embed(title="Error!"))

    async def on_timeout(self) -> None:
        pass


