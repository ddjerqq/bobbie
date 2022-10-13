from disnake.ext import commands
from disnake import ApplicationCommandInteraction as Aci
from client.client import Client, GUILD_IDS
from cogs.admin_panel.admin_services._modal_item_create import ItemCreateModal


class AdminCommands(commands.Cog):
    def __init__(self, client: Client):
        self.client = client
        self.item_create_modal = ItemCreateModal(self.client)

    @commands.slash_command(name="create", guild_ids=GUILD_IDS, description="test features")
    async def create_item(self, inter: Aci):
        if inter.author.id == 725773984808960050:
            await inter.response.send_modal(modal=self.item_create_modal)
        else:
            await inter.send("you can't use that", ephemeral=True)


def setup(client):
    client.add_cog(AdminCommands(client))
