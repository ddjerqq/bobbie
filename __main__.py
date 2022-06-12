import asyncio
import warnings

import disnake
from rgbprint import rgbprint

from client.client import Client


warnings.filterwarnings("ignore")

client = Client(
    help_command=None,
    intents=disnake.Intents.all(),
    case_insensitive=True,
)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(client.start())
        loop.run_forever()

    except KeyboardInterrupt:
        loop.run_until_complete(client.close())

    except Exception as e:
        rgbprint(f"[!!!] {type(e)}\n{e}", color="red")

    finally:
        loop.stop()
        loop.close()
        exit(0)
