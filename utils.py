import os
import random
import asyncio
import disnake
import aiohttp

from rgbprint import rgbprint
from typing import Any
from datetime import datetime

TOKEN = "OTU4MTA3OTA1NzkyNTQ0ODA5.YkIhhQ.YduxqTYY1SVVhQ84C_Ev_WBVC1M"
PREFIX = "!"

_ERROR_FILE_PATH = r".\logs\errors.yandr"
_ERROR_WEBHOOK = "https://discord.com/api/webhooks/" \
                 "958311431617540126/oZynwTGIUNcA2AYYK1y28zgcV3ITK2TZXWGyVcvOVLHs5egkqzBS4Fmsb7e94uYsZvF5"

MESSAGE_DELETE_LOG_CHANNEL_ID = 939534645798793247
CONFESSION_CHANNEL_ID = 958456199148343436


_LOG_FILE = r".\logs\logs.yandr"

GUILD_IDS = [935886444109631510]


async def log_error(message: Any) -> None:
    """
    awaitable coroutine \n
    use this to log errors in logs\\errors.yandr \n
    (red) [!] error \n
    """
    rgbprint("[!]", message, color="red")
    #                        yandr araa sachiro, prosta
    # chemi signature ari, rogorc yandere developer
    # es txt filevit gaixsneba

    if not os.path.exists(_ERROR_FILE_PATH):
        with open(_ERROR_FILE_PATH, "w"):
            pass

    with open(_ERROR_FILE_PATH, "a+", encoding="utf-8") as file:
        file.write(f"[{datetime.now()}]\n{message}\n")

    payload = {"content": f"<@&958110908465442936> unhandled error\n```\n{message}\n```"}
    async with aiohttp.ClientSession() as sesh:
        await sesh.post(_ERROR_WEBHOOK, data=payload)


def log(message: Any) -> None:
    """
    log messages with this
    """
    rgbprint("[+]", message, color = "green")

    if not os.path.exists(_LOG_FILE):
        with open(_LOG_FILE, "w"):
            pass

    with open(_LOG_FILE, "a+", encoding="utf-8") as file:
        file.write(f"[{datetime.now()}]\n{message}\n")



def confession_embed(message: str, author: disnake.Member) -> disnake.Embed:
    embed = disnake.Embed(
        color=0x2d56a9,
        title=message)
    id = random.randint(1_000_000_000, 9_999_999_999)
    embed.set_footer(text=f"ID: {id}")
    log(f"confession with id: {id} was sent by: {author.name}:{author.id}")
    return embed

