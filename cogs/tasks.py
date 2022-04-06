import disnake
from itertools import cycle
from disnake.ext import tasks
from disnake.ext import commands
from models.client import Client


class Tasks(commands.Cog):
    statuses = cycle(["მიეც გლახაკთა საჭურჭლე",
                      "ათავისუფლე მონები",
                      "ddjerqq#2005"])

    def __init__(self, client: Client):
        self.client = client

        self.status_changer.start()
        self.username_updater.start()


    @tasks.loop(seconds=10)
    async def status_changer(self):
        await self.client.change_presence(
            activity=disnake.Game(name=next(self.statuses)))

    @status_changer.before_loop
    async def _statuswait(self):
        await self.client.wait_until_ready()


    @tasks.loop(minutes=30)
    async def username_updater(self):
        for guild in self.client.guilds:
            for member in guild.members:
                if member.bot or member is None:
                    continue

                user = await self.client.db.user_service.get(member.id)

                if user is None:
                    continue

                if member.name != user.username:
                    await self.client.log(f"changed name for {user.username:<32} to {member.name:<32}")
                    user.username = member.name
                    await self.client.db.user_service.update(user)

    @username_updater.before_loop
    async def _usernamewait(self):
        await self.client.wait_until_ready()


def setup(client):
    client.add_cog(Tasks(client))
