from __future__ import annotations
from disnake.ext.commands import CheckFailure
from disnake import ApplicationCommandInteraction as Aci

from client.client import Client
from database import ItemType


__all__ = [
    "check_marriage_target_not_bot",
    "check_marriage_target_not_self",
    "check_marriage_author_has_ring",
    "check_marriage_author_is_not_married_already",
    "check_marriage_target_is_not_married_already",
    "check_divorce_author_is_married_already",

    "TargetBot",
    "MarriageSelfMarriage",
    "MarriageAuthorHasNoRing",
    "MarriageAuthorAlreadyMarried",
    "MarriageTargetAlreadyMarried",
    "DivorceAuthorIsNotMarried",
]


class TargetBot(CheckFailure):...
class MarriageSelfMarriage(CheckFailure):...
class MarriageAuthorHasNoRing(CheckFailure):...
class MarriageAuthorAlreadyMarried(CheckFailure):...
class MarriageTargetAlreadyMarried(CheckFailure):...
class DivorceAuthorIsNotMarried(CheckFailure):...


async def check_marriage_target_not_bot(inter: Aci) -> bool:
    target = inter.filled_options.get("target", None)
    if target.bot:
        raise TargetBot()
    return True


async def check_marriage_target_not_self(inter: Aci) -> bool:
    target = inter.filled_options.get("target", None)
    if target == inter.author:
        raise MarriageSelfMarriage()
    return True


async def check_marriage_author_has_ring(inter: Aci) -> bool:
    client: Client = inter.bot  # type: ignore
    user = await client.db.users.get(inter.author.id)
    if not any(it.type == ItemType.WEDDING_RING for it in user.items):
        raise MarriageAuthorHasNoRing()
    else:
        return True


async def check_marriage_author_is_not_married_already(inter: Aci) -> bool:
    client: Client = inter.bot  # type: ignore
    user = await client.db.users.get(inter.author.id)
    if user.marriage_id:
        raise MarriageAuthorAlreadyMarried()
    return True


async def check_marriage_target_is_not_married_already(inter: Aci) -> bool:
    client: Client = inter.bot  # type: ignore
    target = inter.filled_options.get("target", None)
    target = await client.db.users.get(target.id)
    if target.marriage_id:
        raise MarriageTargetAlreadyMarried()
    return True


async def check_divorce_author_is_married_already(inter: Aci) -> bool:
    client: Client = inter.bot  # type: ignore
    user = await client.db.users.get(inter.author.id)
    if not user.marriage_id:
        raise DivorceAuthorIsNotMarried()
    return True
