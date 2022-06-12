import disnake
from disnake.ext import tasks
from disnake.ext import commands
from client import Client


class StatusChanger(commands.Cog):
    def __init__(self, client: Client):
        self.client = client
        self.status_changer.start()

    @tasks.loop(seconds=5)
    async def status_changer(self):
        await self.client.change_presence(
            activity=disnake.Game(
                name=next(self.client.statuses)
            )
        )

    @status_changer.before_loop
    async def _before_status_changer(self):
        await self.client.wait_until_ready()


def setup(client):
    client.add_cog(StatusChanger(client))
