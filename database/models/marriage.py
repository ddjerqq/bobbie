from __future__ import annotations

import datetime
from database.id import Id


class Marriage:
    def __init__(self,
                 id: int,
                 king_id: int,
                 bride_id: int,
                 guild_id: int,
                 bride_role_id: int,
                 king_role_id: int) -> None:
        self.__id          = id
        self.king_id       = king_id
        self.bride_id      = bride_id
        self.guild_id      = guild_id
        self.bride_role_id = bride_role_id
        self.king_role_id  = king_role_id

    @property
    def id(self) -> int:
        return self.__id

    @property
    def created_at(self) -> datetime.datetime:
        return Id.created_at(self.__id)

    @property
    def db_dict(self) -> dict:
        return {
            "id": self.__id,
            "king_id": self.king_id,
            "bride_id": self.bride_id,
            "guild_id": self.guild_id,
            "bride_role_id": self.bride_role_id,
            "king_role_id": self.king_role_id,
        }

    def __hash__(self):
        return hash(self.__id)

    def __eq__(self, other):
        return isinstance(other, Marriage) and self.__id == other.__id

    def __str__(self):
        return f"Marriage {self.king_id} married to {self.bride_id}"

    def __repr__(self):
        return f"<Item id={self.__id} {self.king_id} married to {self.bride_id} created_at={self.created_at}>"
