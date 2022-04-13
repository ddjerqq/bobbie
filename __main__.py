# from templates import *  # THIS IS IMPORTANT WE NEED TO INITIALIZE THE OPTIONS FIRST
import sys
import disnake
import asyncio
from utils import *
from rgbprint import rgbprint
from models.client import Client


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

        if len(sys.argv) == 2 and sys.argv[1] == "--dev-test":
            loop.run_until_complete(client.start(DEV_TEST_TOKEN))
        else:
            loop.run_until_complete(client.start(TOKEN))

    except KeyboardInterrupt:
        loop.run_until_complete(client.close())

    except Exception as e:
        rgbprint(f"[!!!] {type(e)}\n{e}", color="red")

    finally:
        loop.run_until_complete(asyncio.sleep(1))
        loop.close()
