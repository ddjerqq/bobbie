import random

import disnake
from client.client import Client


class UtilityService:
    def __init__(self, client: Client):
        self.__client = client

    def avatar(self, target: disnake.Member) -> disnake.Embed:
        em = disnake.Embed(
            title=f"{target.name}'ს ავატარი",
            color=0x2d56a9
        )
        em.set_footer(text=f"ID: {target.id}")
        em.set_image(url=target.avatar.url)
        return em

    def info(self, target: disnake.Member) -> disnake.Embed:
        em = disnake.Embed(
            title=f"{target.name}'ს ინფო",
            color=0x2d56a9
        )
        em.add_field(
            name="რეგისტრაცია",
            value=target.created_at.strftime("%d-%m-%y %H:%M:%S"),
            inline=False
        )
        em.add_field(
            name="დაჯოინდა",
            value=target.joined_at.strftime("%d-%m-%Y"),
            inline=False
        )
        em.add_field(
            name=f"{target.name}'ს როლები",
            value=", ".join(map(lambda r: r.name, target.roles)),
            inline=False
        )

        em.set_thumbnail(url=target.avatar.url)
        em.set_footer(text=f"ID: {target.id}")

        return em

