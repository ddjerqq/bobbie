import asyncio

import disnake
from itertools import cycle
from disnake.ext import tasks
from disnake.ext import commands
from models.client import Client
from models.user import User
from utils import STATUSES


class Tasks(commands.Cog):
    statuses = cycle(STATUSES)

    def __init__(self, client: Client):
        self.client = client

        self.status_changer.start()
        self.username_updater.start()


    @tasks.loop(seconds=5)
    async def status_changer(self):
        await self.client.change_presence(
            activity=disnake.Game(name=next(self.statuses)))

    @status_changer.before_loop
    async def _statuswait(self):
        await self.client.wait_until_ready()


    @tasks.loop(minutes=60)
    async def username_updater(self):
        for guild in self.client.guilds:
            for member in guild.members:
                if member.bot or member is None:
                    continue

                user = await self.client.db.user_service.get(member.id)

                if isinstance(user, User):
                    if member.name != user.username:
                        await self.client.log(f"changed name for {user.username:<32} to {member.name:<32}")
                        user.username = member.name
                        await self.client.db.user_service.update(user)
                elif user is None:
                    await self.client.db.user_service.add(member.id, member.name)
                    await self.client.log(f"added ({member.id}) {member.name}")
                else:
                    continue


    @username_updater.before_loop
    async def _usernamewait(self):
        await asyncio.sleep(10)
        await self.client.wait_until_ready()


def setup(client):
    client.add_cog(Tasks(client))
