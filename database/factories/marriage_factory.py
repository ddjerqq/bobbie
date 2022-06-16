import sqlite3

import disnake

from database.id import Id
from database.models.marriage import Marriage

import typing
if typing.TYPE_CHECKING:
    from database.models.user import User


class MarriageFactory:
    def __init__(self, client):
        self.__client = client

    @classmethod
    def new(cls,
            king: disnake.Member,
            bride: disnake.Member,
            guild: disnake.Guild,
            bride_role: disnake.Role,
            king_role: disnake.Role) -> Marriage:
        """
        create a new marriage with a random id, and role and married to generation
        """
        id = Id.new()
        marriage = Marriage(id, king.id, bride.id, guild.id, bride_role.id, king_role.id)
        return marriage

    @classmethod
    def from_db_row(cls, data: tuple[int, int, int, int, int, int] | sqlite3.Row) -> Marriage:
        return Marriage(*data)
