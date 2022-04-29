import disnake
from disnake import ui
from disnake import MessageInteraction as Mi
from disnake.ext import commands
from disnake import ApplicationCommandInteraction as Aci

from database.models.item import Item
from client import *


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



class TicTacToeView(ui.View):
    def __init__(self, player_one: disnake.Member, player_two: disnake.Member, *, timeout: float = 180):
        super().__init__(timeout=timeout)
        self._player_one = player_one
        self._player_two = player_two
        self.board = [[-1, -1, -1],
                      [-1, -1, -1],
                      [-1, -1, -1]]  # type: list[list[int]]

    @ui.button(label=".", style=disnake.ButtonStyle.gray, row=1)
    async def _button1(self, button: disnake.Button, inter: Mi):
        if inter.author != self._player_one and inter.author != self._player_two:
            await inter.send("ეს შენთვის არაა! ;)", ephemeral=True)
            return
        for row in self.board:
            for cell in row:
                if cell is None:
                    continue
        if inter.author == self._player_one:
            self.board[0][0] = 0
            button.label = "X"
            button.style = disnake.ButtonStyle.green
        else:
            self.board[0][0] = 1
            button.label = "O"
            button.style = disnake.ButtonStyle.danger
        button.disabled = True

    @ui.button(label=".", style=disnake.ButtonStyle.gray, row=1)
    async def _button2(self, button: disnake.Button, inter: Mi):
        if inter.author != self._player_one and inter.author != self._player_two:
            await inter.send("ეს შენთვის არაა! ;)", ephemeral=True)
            return
        for row in self.board:
            for cell in row:
                if cell is None:
                    continue
        if inter.author == self._player_one:
            self.board[0][1] = 0
            button.label = "X"
            button.style = disnake.ButtonStyle.green
        else:
            self.board[0][1] = 1
            button.label = "O"
            button.style = disnake.ButtonStyle.danger
        button.disabled = True

    @ui.button(label=".", style=disnake.ButtonStyle.gray, row=1)
    async def _button3(self, button: disnake.Button, inter: Mi):
        if inter.author != self._player_one and inter.author != self._player_two:
            await inter.send("ეს შენთვის არაა! ;)", ephemeral=True)
            return
        for row in self.board:
            for cell in row:
                if cell is None:
                    continue
        if inter.author == self._player_one:
            self.board[0][2] = 0
            button.label = "X"
            button.style = disnake.ButtonStyle.green
        else:
            self.board[0][2] = 1
            button.label = "O"
            button.style = disnake.ButtonStyle.danger
        button.disabled = True


    @ui.button(label=".", style=disnake.ButtonStyle.gray, row=2)
    async def _button4(self, button: disnake.Button, inter: Mi):
        if inter.author != self._player_one and inter.author != self._player_two:
            await inter.send("ეს შენთვის არაა! ;)", ephemeral=True)
            return
        for row in self.board:
            for cell in row:
                if cell is None:
                    continue
        if inter.author == self._player_one:
            self.board[1][0] = 0
            button.label = "X"
            button.style = disnake.ButtonStyle.green
        else:
            self.board[1][0] = 1
            button.label = "O"
            button.style = disnake.ButtonStyle.danger
        button.disabled = True

    @ui.button(label=".", style=disnake.ButtonStyle.gray, row=2)
    async def _button5(self, button: disnake.Button, inter: Mi):
        if inter.author != self._player_one and inter.author != self._player_two:
            await inter.send("ეს შენთვის არაა! ;)", ephemeral=True)
            return
        for row in self.board:
            for cell in row:
                if cell is None:
                    continue
        if inter.author == self._player_one:
            self.board[1][1] = 0
            button.label = "X"
            button.style = disnake.ButtonStyle.green
        else:
            self.board[1][1] = 1
            button.label = "O"
            button.style = disnake.ButtonStyle.danger
        button.disabled = True

    @ui.button(label=".", style=disnake.ButtonStyle.gray, row=2)
    async def _button6(self, button: disnake.Button, inter: Mi):
        if inter.author != self._player_one and inter.author != self._player_two:
            await inter.send("ეს შენთვის არაა! ;)", ephemeral=True)
            return
        for row in self.board:
            for cell in row:
                if cell is None:
                    continue
        if inter.author == self._player_one:
            self.board[1][2] = 0
            button.label = "X"
            button.style = disnake.ButtonStyle.green
        else:
            self.board[1][2] = 1
            button.label = "O"
            button.style = disnake.ButtonStyle.danger
        button.disabled = True


    @ui.button(label=".", style=disnake.ButtonStyle.gray, row=3)
    async def _button7(self, button: disnake.Button, inter: Mi):
        if inter.author != self._player_one and inter.author != self._player_two:
            await inter.send("ეს შენთვის არაა! ;)", ephemeral=True)
            return
        for row in self.board:
            for cell in row:
                if cell is None:
                    continue
        if inter.author == self._player_one:
            self.board[2][0] = 0
            button.label = "X"
            button.style = disnake.ButtonStyle.green
        else:
            self.board[2][0] = 1
            button.label = "O"
            button.style = disnake.ButtonStyle.danger
        button.disabled = True

    @ui.button(label=".", style=disnake.ButtonStyle.gray, row=3)
    async def _button8(self, button: disnake.Button, inter: Mi):
        if inter.author != self._player_one and inter.author != self._player_two:
            await inter.send("ეს შენთვის არაა! ;)", ephemeral=True)
            return
        for row in self.board:
            for cell in row:
                if cell is None:
                    continue
        if inter.author == self._player_one:
            self.board[2][1] = 0
            button.label = "X"
            button.style = disnake.ButtonStyle.green
        else:
            self.board[2][1] = 1
            button.label = "O"
            button.style = disnake.ButtonStyle.danger
        button.disabled = True

    @ui.button(label=".", style=disnake.ButtonStyle.gray, row=3)
    async def _button9(self, button: disnake.Button, inter: Mi):
        if inter.author != self._player_one and inter.author != self._player_two:
            await inter.send("ეს შენთვის არაა! ;)", ephemeral=True)
            return
        for row in self.board:
            for cell in row:
                if cell is None:
                    continue
        if inter.author == self._player_one:
            self.board[2][2] = 0
            button.label = "X"
            button.style = disnake.ButtonStyle.green
        else:
            self.board[2][2] = 1
            button.label = "O"
            button.style = disnake.ButtonStyle.danger
        button.disabled = True


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


    @commands.slash_command(name="tictactoe", guild_ids=GUILD_IDS, description="test features")
    async def tictactoe(self, inter: Aci, player: disnake.Member):
        v = TicTacToeView(inter.author, player)
        await inter.send(view=v)
        await v.wait()

        await inter.send(v.board)


def setup(client):
    client.add_cog(FeatureTests(client))
