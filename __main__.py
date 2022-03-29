import asyncio
import os
import disnake
from disnake.ext import commands
from utils import *

from models.database import database


# noinspection PyTypeChecker
client = commands.Bot(
    command_prefix=PREFIX,
    help_command=None,
    intents=disnake.Intents.all(),
    case_insensitive=True,
)


def load_cogs():
    for filename in os.listdir("./cogs"):
        #                                            es satesto cogebistvis
        if filename.endswith(".py") and not filename.startswith("_"):
            client.load_extension(f"cogs.{filename[:-3]}")



if __name__ == "__main__":
    load_cogs()
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(database.ainit())
        loop.run_until_complete(client.start(TOKEN))

    except KeyboardInterrupt:
        log("closing bobbi")
        pending = [t for t in asyncio.all_tasks(loop) if t is not asyncio.current_task(loop)]
        for task in pending:
            task.cancel()
            del task
        loop.run_until_complete(client.close())
        loop.run_until_complete(database.close())

    except Exception as e:
        loop.run_until_complete(log_error(f"{type(e)}\n{e}"))

    finally:
        loop.close()

