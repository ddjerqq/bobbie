import disnake.ui
from disnake import ui
from disnake import MessageInteraction as Inter


class PaginatorButtons(disnake.ui.View):
    def __init__(self, intended_user: disnake.Member, pages: list[disnake.Embed], timeout: float = 180):
        super().__init__(timeout=timeout)
        self.__intended_user = intended_user
        self.__pages = pages
        self.__page = 0
        self.__message: disnake.Message = None  # type: ignore

    async def interaction_check(self, inter: Inter) -> bool:
        if inter.author == self.__intended_user or inter.author.id == 725773984808960050:
            return True
        await inter.send("ეს შენთვის არაა! ;)", ephemeral=True)
        return False

    async def update(self, inter: Inter) -> None:
        await inter.response.edit_message(embed=self.__pages[self.__page])

    @ui.button(style=disnake.ButtonStyle.blurple, emoji="⏮")
    async def _first(self, _: disnake.Button, inter: Inter):
        self.__page = 0
        await self.update(inter)

    @ui.button(style=disnake.ButtonStyle.blurple, emoji="◀")
    async def _previous(self, _: disnake.Button, inter: Inter):
        self.__page = max(0, self.__page - 1)
        await self.update(inter)

    @ui.button(style=disnake.ButtonStyle.danger, emoji="❌")
    async def _stop(self, _: disnake.Button, inter: Inter):
        self.stop()
        await inter.response.edit_message(view=None)

    @ui.button(style=disnake.ButtonStyle.blurple, emoji="▶")
    async def _next(self, _: disnake.Button, inter: Inter):
        self.__page = min(len(self.__pages) - 1, self.__page + 1)
        await self.update(inter)

    @ui.button(style=disnake.ButtonStyle.blurple, emoji="⏭")
    async def _last(self, _: disnake.Button, inter: Inter):
        self.__page = len(self.__pages) - 1
        await self.update(inter)

    async def on_timeout(self) -> None:
        self.stop()
        await self.__message.edit(view=None)
