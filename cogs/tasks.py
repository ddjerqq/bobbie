from services.user_service import *
from disnake.ext import commands
from disnake.ext import tasks
from itertools import cycle
from utils import *
import disnake


class Tasks(commands.Cog):
    statuses = cycle(["Campfire stories 🔥",
                      "be nice",
                      "გივევეიები ყოველ კვირა!",
                      "frosty-ს დიდი ყლე აქვს"])

    def __init__(self, client: disnake.Client):
        self.client = client

        self.status_changer.start()
        self.username_updater.start()


    @tasks.loop(seconds=10)
    async def status_changer(self):
        await self.client.change_presence(
            activity=disnake.Game(name=next(self.statuses))
        )

    @status_changer.before_loop
    async def _statuswait(self):
        await self.client.wait_until_ready()


    @tasks.loop(minutes=60)
    async def username_updater(self):
        for guild in self.client.guilds:
            for member in filter(lambda m: not m.bot, guild.members):
                user = await get_by_id(member.id)

                if user is None:
                    continue

                if member.name != user.username:
                    log(f"changed name for {user.username:<32} to {member.name:<32}")
                    await update_username(member.id, member.name)

    @username_updater.before_loop
    async def _usernamewait(self):
        await self.client.wait_until_ready()

    @tasks.loop(minutes=5)
    async def database_save(self):
        await database.save()

    @database_save.before_loop
    async def _databasewait(self):
        await self.client.wait_until_ready()



def setup(client):
    client.add_cog(Tasks(client))
