from itertools import cycle

import disnake
from disnake.ext import tasks
from disnake.ext import commands
from client.client import Client


class StatusChanger(commands.Cog):
    def __init__(self, client: Client):
        self.client = client
        self.status_changer.start()
        self.statuses = cycle([
            "მიეც გლახაკთა საჭურჭლე,",
            "ათავისუფლე მონები.",
            "ddjerqq#2005",
            "სიკვდილი ყველას გვაშინებს,",
            "სხვას თუ ჰკვლენ, ცქერა გვწადიან.",
            "დღეს სტუმარია ეგ ჩემი,",
            "თუნდ ზღვა ემართოს სისხლისა.",
        ])

    @tasks.loop(seconds=5)
    async def status_changer(self):
        await self.client.change_presence(
            activity=disnake.Game(
                name=next(self.statuses)
            )
        )

    @status_changer.before_loop
    async def _before_status_changer(self):
        await self.client.wait_until_ready()


def setup(client):
    client.add_cog(StatusChanger(client))
