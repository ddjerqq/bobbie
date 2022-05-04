import os
import sys
from itertools import cycle
import disnake
import asyncio
from typing import Any
from rgbprint import rgbprint
from disnake.ext import commands
from database import Database
from client.embed_service import EmbedService
from client.button_service import Buttons


PROJECT_PATH = os.getcwd()
DEV_TEST     = len(sys.argv) == 2 and sys.argv[1] == "--dev-test"
GUILD_IDS    = None if not DEV_TEST else [965308417185021982]
# 965308417185021982
# 935886444109631510
# 840836206483734530
# 913003554225131530


class Client(commands.Bot):
    __TOKEN          = "OTU4MTA3OTA1NzkyNTQ0ODA5.YkIhhQ.YduxqTYY1SVVhQ84C_Ev_WBVC1M"
    __DEV_TEST_TOKEN = "OTYzNDU3MTI4MzM1NTUyNTUy.YlWXXw.n7uo7VtPt_4VRUDMiaqYYlzWUx0"
    PREFIX           = "!"

    DELETE_MESSAGE_LOG    = 939534645798793247
    CONFESSION_CHANNELS   = [958456199148343436]
    LOG_CHANNEL_ID        = 958311400047001600
    LEAVE_CHANNEL_ID      = 942800528822370315

    def __init__(self, *args, **kwargs):
        self.db             = Database()
        self.embeds         = EmbedService(self.db)
        self.button_service = Buttons()
        self.log_channel    = None  # type: disnake.TextChannel
        self.statuses       = cycle([
            "მიეც გლახაკთა საჭურჭლე,",
            "ათავისუფლე მონები.",
            "ddjerqq#2005",
            "სიკვდილი ყველას გვაშინებს,",
            "სხვას თუ ჰკვლენ, ცქერა გვწადიან.",
            "დღეს სტუმარია ეგ ჩემი,",
            "თუნდ ზღვა ემართოს სისხლისა.",
        ])
        self.command_prefix = self.PREFIX
        self.wordle_words   = []  # type: list[str]

        super().__init__(*args, **kwargs)
        self._load_extensions()
        self._load_words()

    async def start(self) -> None:
        await super().start(self.__TOKEN if not DEV_TEST else self.__DEV_TEST_TOKEN)

    def _load_extensions(self) -> None:
        for cog in os.listdir(f"{PROJECT_PATH}/cogs"):
            if cog.endswith(".py") and not cog.startswith("_"):
                self.load_extension(f"cogs.{cog[:-3]}")

    def _load_words(self) -> None:
        with open(f"{PROJECT_PATH}/assets/unverified_words.txt", encoding="utf-8") as f:
            self.wordle_words = [w.strip() for w in f.readlines() if w]

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
