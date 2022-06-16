import disnake


class GenericEmbedService:
    def __init__(self, client):
        self.__client = client

    def generic_success(self, title: str = "წარმატება!", description: str = None) -> disnake.Embed:
        em = disnake.Embed(color=0x2B693A, title=title)
        if description:
            em.description = description
        return em

    def generic_error(self, title: str = "წარუმატებლობა!", description: str = None) -> disnake.Embed:
        em = disnake.Embed(color=0xB10F28, title=title)
        if description:
            em.description = description
        return em

