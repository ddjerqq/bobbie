import datetime
from itertools import cycle

import disnake
from disnake.ext import tasks
from disnake.ext import commands
from client.client import Client


TIMES = (datetime.time(12, 0, 0), datetime.time(24, 0, 0))


class NightModeChanger(commands.Cog):
    def __init__(self, client: Client):
        self.client = client
        self.general = client.get_channel(935887688085680128)
        self.night_emoji_cycle = cycle(["🌙", "🌚"])

    @tasks.loop(time=TIMES)
    async def night_emoji(self):
        await self.general.edit(name=f"・general {next(self.night_emoji_cycle)}")

    @night_emoji.before_loop
    async def wait_until_time(self):
        await self.client.wait_until_ready()


def setup(client):
    client.add_cog(NightModeChanger(client))
