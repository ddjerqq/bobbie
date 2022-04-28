# from templates import *  # THIS IS IMPORTANT WE NEED TO INITIALIZE THE OPTIONS FIRST
import asyncio
import time

import disnake
from rgbprint import rgbprint

from client import Client
from utils import *

client = Client(
    command_prefix=PREFIX,
    help_command=None,
    intents=disnake.Intents.all(),
    case_insensitive=True,
)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(client.db.ainit())

        if DEV_TEST:
            loop.run_until_complete(client.start(DEV_TEST_TOKEN))
        else:
            loop.run_until_complete(client.start(TOKEN))

    except KeyboardInterrupt:
        loop.run_until_complete(client.close())

    except Exception as e:
        rgbprint(f"[!!!] {type(e)}\n{e}", color="red")

    finally:
        loop.close()
        time.sleep(0.2)
        exit(0)
