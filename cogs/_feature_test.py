import disnake
from disnake import ui
from disnake import MessageInteraction as Mi
from disnake.ext import commands
from disnake import ApplicationCommandInteraction as Aci

from models.item import Item
from utils import *
from models.client import Client




class TestView(ui.View):
    def __init__(self, *, timeout: float = 180, intended_user: disnake.Member = None):
        super().__init__(timeout=timeout)
        self._intended_user = intended_user
        self.choice = None

    @ui.button(label="კი", style=disnake.ButtonStyle.green)
    async def _yes(self, _: disnake.Button, inter: Mi):
        if self._intended_user is not None and inter.author != self._intended_user:
            await inter.send("ეს შენთვის არაა! ;)", ephemeral=True)
            return
        self.choice = True
        self.stop()

    @ui.button(label="არა", style=disnake.ButtonStyle.danger)
    async def _no(self, _: disnake.Button, inter: Mi):
        if self._intended_user is not None and inter.author != self._intended_user:
            await inter.send("ეს შენთვის არაა! ;)", ephemeral=True)
            return
        self.choice = False
        self.stop()


    @ui.select(options=[
        disnake.SelectOption(label="ტესტი გიო მაგარია", value="test",
                             description="description", emoji="💀"),
        disnake.SelectOption(label="ტესტი ორი ფროსტიც მაგარია", value="test2",
                             description="description", emoji="👽"),
    ])
    async def select(self, select: ui.Select, inter: Mi):
        print(select.values)
        print(select)
        print(inter)





class MyModal(ui.Modal):
    def __init__(self):
        components = [
            ui.TextInput(
                label="type",
                placeholder="enter item type",
                custom_id="type",
                max_length=16,
            ),
            ui.TextInput(
                label="rarity",
                placeholder="enter item rarity",
                custom_id="rarity"
            ),
        ]
        super().__init__(
            title="create item",
            custom_id="create_item",
            components=components
        )

    async def callback(self, inter: disnake.ModalInteraction, /) -> None:
        embed = disnake.Embed(title="Item Created")
        type = inter.text_values.get("type")
        rarity = inter.text_values.get("rarity")
        item = Item.new(type)
        item._rarity = float(rarity)
        item.owner_id = inter.author.id
        embed.title += item.emoji
        if item.thumbnail:
            embed.set_thumbnail(url=item.thumbnail)
        embed.add_field(name="item type", value=item.name)
        embed.add_field(name="item rarity", value=f"{item.rarity} - {item.rarity_string}")
        embed.add_field(name="item price", value=item.price)
        embed.set_footer(text=f"ID: {item.id} owner: {item.owner_id}")

        await inter.response.send_message(embed=embed)





class FeatureTests(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    @commands.slash_command(name="test", guild_ids=GUILD_IDS, description="test features")
    async def test(self, inter: Aci):
        v = TestView()
        await inter.send(view=v)
        await v.wait()
        if v.choice:
            await inter.send("hello")
        else:
            await inter.send("goodbye")


    @commands.slash_command(name="modal", guild_ids=GUILD_IDS, description="test features")
    async def modal(self, inter: Aci):
        modal = MyModal()
        await inter.response.send_modal(modal=modal)



def setup(client):
    client.add_cog(FeatureTests(client))
