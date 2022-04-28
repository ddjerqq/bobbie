import asyncio

import disnake
from disnake.ext import tasks
from disnake.ext import commands
from client import Client
from database.models.user import User


class Tasks(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

        self.status_changer.start()
        self.username_updater.start()


    @tasks.loop(seconds=5)
    async def status_changer(self):
        await self.client.change_presence(activity=disnake.Game(name=next(self.client.statuses)))

    @status_changer.before_loop
    async def _statuswait(self):
        await self.client.wait_until_ready()


    @tasks.loop(minutes=10)
    async def username_updater(self):
        for guild in self.client.guilds:
            for member in guild.members:
                if member.bot or member is None:
                    continue

                user = await self.client.db.users.get(member.id)

                if isinstance(user, User):
                    if member.name != user.username:
                        await self.client.log(f"changed name for {user.username} to {member.name}")
                        user.username = member.name
                        await self.client.db.users.update(user)
                elif user is None:
                    await self.client.db.users.add(member.id, member.name)
                    await self.client.log(f"added ({member.id}) {member.name}")


    @username_updater.before_loop
    async def _usernamewait(self):
        await asyncio.sleep(10)
        await self.client.wait_until_ready()


def setup(client):
    client.add_cog(Tasks(client))
