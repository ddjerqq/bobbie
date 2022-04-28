import disnake
from disnake import ui
from disnake import MessageInteraction as Mi


class Buttons:
    class YesNoButton(ui.View):
        """
        Starndard Yes No button, with კი and არა as their choices
        if intended_user is passed it will be used to set the intended user
        if the intended user it not None and someone else tries to use the button, the bot will
        send an ephemeral message to the unintended member
        """
        def __init__(self, *, timeout: float = 180, intended_user: disnake.Member = None):
            super().__init__(timeout=timeout)
            self._intended_user = intended_user
            self.choice = None

        @ui.button(label="კი", style=disnake.ButtonStyle.green)
        async def _yes(self, _: disnake.Button, inter: Mi):
            if self._intended_user is not None:
                if inter.author != self._intended_user:
                    await inter.send("ეს შენთვის არაა! ;)", ephemeral=True)
                else:
                    self.choice = True
                    self.stop()

        @ui.button(label="არა", style=disnake.ButtonStyle.danger)
        async def _no(self, _: disnake.Button, inter: Mi):
            if self._intended_user is not None:
                if inter.author != self._intended_user:
                    await inter.send("ეს შენთვის არაა! ;)", ephemeral=True)
                else:
                    self.choice = False
                    self.stop()

