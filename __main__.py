import asyncio
import disnake
from client.client import Client
from client.logger import LogLevel

client = Client(
    help_command=None,
    intents=disnake.Intents.all(),
    case_insensitive=True,
)


async def main():
    try:
        await client.start()
    except KeyboardInterrupt:
        await client.close()
    except Exception as e:
        await client.logger.log(e, level=LogLevel.ERROR)
        await client.close()
    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(main())
