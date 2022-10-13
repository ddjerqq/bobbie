import asyncio
import disnake
from client.client import Client
from client.logger import LogLevel

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

client = Client(
    help_command=None,
    intents=disnake.Intents.all(),
    case_insensitive=True,
)


def main():
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(client.start())
    except KeyboardInterrupt:
        loop.run_until_complete(client.close())
    except Exception as e:
        loop.run_until_complete(client.logger.log(e, level=LogLevel.ERROR))
    finally:
        loop.run_until_complete(client.close())
        loop.close()


if __name__ == "__main__":
    main()
