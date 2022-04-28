import os
from itertools import cycle
import disnake
import asyncio
from typing import Any
from rgbprint import rgbprint
from disnake.ext import commands
from database import Database
from client.embed_service import EmbedService
from client.button_service import Buttons
from utils import PROJECT_PATH


class Client(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._load_extensions()

        self.db = Database()
        self.embeds  = EmbedService(self.db)
        self.button_service = Buttons()

        self.log_channel: disnake.TextChannel | None  = None
        self.statuses = cycle([
            "მიეც გლახაკთა საჭურჭლე,",
            "ათავისუფლე მონები.",
            "ddjerqq#2005",
            "სიკვდილი ყველას გვაშინებს,",
            "სხვას თუ ჰკვლენ, ცქერა გვწადიან.",
            "დღეს სტუმარია ეგ ჩემი,",
            "თუნდ ზღვა ემართოს სისხლისა.",
        ])


    def _load_extensions(self) -> None:
        for cog in os.listdir(f"{PROJECT_PATH}\\cogs"):
            if cog.endswith(".py") and not cog.startswith("_"):
                self.load_extension(f"cogs.{cog[:-3]}")


    async def close(self):
        await self.log("cancelling tasks")
        pending = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        for t in pending:
            t.cancel()
        await self.log("cancelled  tasks")
        await self.log("closing   client")
        await super().close()
        await self.log("closed    client")


    async def log(self, message: Any, priority: int = 3) -> None:
        """
        |coro|
        log messages with priorities (red) [!] error \n

        :param message: message to log, it can be any type
        :param priority: priority for the log, 3 log. 2 warn. 1 error
        """
        match priority:
            case 3:
                prefix = "[+]"
                color  = "green"
                log_type = "log"

            case 2:
                prefix = "[-]"
                color  = "yellow"
                log_type = "warn"

            case 1:
                prefix = "[!]"
                color  = "red"
                log_type = "error"

            case _:
                prefix, color, log_type = None, None, None

        rgbprint(prefix, color=color, sep="", end=" ")
        rgbprint(message)

        if priority <= 2:
            if self.log_channel is not None:
                await self.log_channel.send(f"*`{log_type}`*```{message}```")
            else:
                rgbprint("warn-error log channel not configured")
