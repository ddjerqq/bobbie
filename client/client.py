import os
import toml
import pathlib
import asyncio
from disnake.ext import commands

from logger import Logger
from database import Database
from services.embed_services.embed_service import EmbedService
from services.view_services.button_service import Buttons
from dotenv import load_dotenv

load_dotenv()

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG       = toml.load(os.path.join(PROJECT_PATH, "bobbie.toml"))
DEV_TEST     = CONFIG["bot"]["testing"]
GUILD_IDS    = None if not DEV_TEST else [CONFIG["bot"]["test_guild_id"]]


class Client(commands.Bot):
    __TOKEN          = os.getenv("PROD_TOKEN")
    __TEST_TOKEN     = os.getenv("TEST_TOKEN")

    DELETE_MESSAGE_LOG  = CONFIG["channels"]["deleted_msgs"]
    CONFESSION_CHANNELS = CONFIG["channels"]["confessions"]
    LOG_CHANNEL_ID      = CONFIG["channels"]["logging"]
    LEAVE_CHANNEL_ID    = CONFIG["channels"]["leave"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db             = None  # type: Database | None
        self.logger         = Logger(self)
        self.embeds         = EmbedService(self.db)
        self.buttons        = Buttons()
        self.config         = CONFIG
        self.command_prefix = CONFIG["bot"]["prefix"]
        self.__load_extensions()

    def __load_extensions(self) -> None:
        for root, _, files in os.walk(os.path.join(PROJECT_PATH, "cogs")):
            for cog in files:
                if cog.endswith(".py"):
                    cog = cog.removesuffix(".py")
                if cog.startswith("_"):
                    continue
                folder = pathlib.Path(root).name
                cog = f"cogs.{folder}.{cog}"
                self.load_extension(cog)

    async def start(self, *_) -> None:
        self.db = Database.ainit(PROJECT_PATH)
        await super().start(self.__TOKEN if not DEV_TEST else self.__TEST_TOKEN)

    async def close(self):
        pending = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        for t in pending:
            t.cancel()
        await super().close()
