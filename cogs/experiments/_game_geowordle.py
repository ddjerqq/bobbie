import asyncio
import random
import string

import disnake
from disnake import ApplicationCommandInteraction as Aci
from disnake.ext import commands

from client.client import Client


class GeoWordleGame(commands.Cog):
    def __init__(self, client: Client):
        self.client = client

    @commands.slash_command(name="geowordle", guild_ids=[965308417185021982], description="ითამაშეთ worlde ქართულად")
    async def geowordle(self, inter: Aci):
        # -1 light gray
        #  0 black
        #  1 yellow
        #  2 green

        win_prizes = {
            0: 10_000,
            1: 7_500,
            2: 5_000,
            3: 3_000,
            4: 2_000,
            5: 1_000,
            6: 500,
            7: 100,
        }

        grid = [[-1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1]]

        has   = set()
        hasnt = set()
        index = {}

        secret_word = random.choice(self.client.wordle_words)

        em = self.client.embeds.wordle_grid(grid, author=inter.author)
        await inter.send(embed=em, delete_after=10)

        old = None
        turn = 0

        geo_letters = set("აბგდევზთიკლმნოპჟრსტუფქღყშჩცძწჭხჯჰ")

        while turn < len(grid):
            try:
                msg = await self.client.wait_for("message",
                                                 check=lambda m: m.author == inter.author
                                                                 and
                                                                 m.channel == inter.channel
                                                                 and
                                                                 len(m.content) == 5
                                                                 and
                                                                 not any(c in string.punctuation for c in m.content)
                                                                 and
                                                                 all(c in geo_letters for c in m.content),
                                                 timeout=60
                                                 )
            except asyncio.exceptions.TimeoutError:
                await inter.send(embed=self.client.embeds.generic_error("1 წუთი გავიდა!!"))
                return

            word = msg.content
            await msg.delete()

            for idx, (char_guess, char_secret) in enumerate(zip(word, secret_word)):
                if char_guess == char_secret:
                    has.add(char_guess)
                    index[idx] = char_guess
                    grid[turn][idx] = 2
                elif char_guess not in secret_word:
                    grid[turn][idx] = 0
                    hasnt.add(char_guess)
                elif char_guess in secret_word:
                    grid[turn][idx] = 1
                    has.add(char_guess)

            em = self.client.embeds.wordle_grid(grid, has=has, hasnt=hasnt, index=index, author=inter.author)
            em.title = f"{word} | {inter.author.name}"

            if old:
                await old.delete()
            old = await inter.followup.send(embed=em)

            if word == secret_word:
                em = disnake.Embed(color=0x00ff00)
                em.title = f"თქვენ გამოიცანით!"
                em.description = f"სიტყვა იყო {secret_word}, \nშენ მოიგე {win_prizes[turn]}₾"
                user = await self.client.db.users.get(inter.author.id)
                user.wallet += win_prizes[turn]
                await self.client.db.users.update(user)
                await inter.send(embed=em)
                return

            turn += 1

        else:
            await old.delete()
            em = disnake.Embed(color=0xff0000)
            em.title = f"შენ ვერ გამოიცანი!,\nსიტყვა იყო {secret_word}"
            await inter.send(embed=em)



    @commands.slash_command(name="filter",
                            guild_ids=[965308417185021982,
                                       965308417185021982,
                                       935886444109631510],
                            description="გაფილტრე სიტყვები და მიიღე 10₾ თითოში")
    async def filter_words(self, inter: Aci):
        earned = 0
        await inter.send("შენ დაიწყე მუშაობა! თითო სიტყვის ვერიფიკაციით შენ მიიღებ ჯილდოს", delete_after=10)

        while True:
            word = (await self.client.db.unverified_word())[0]

            button = self.client.button_service.YesNoIdk(intended_user=inter.author, timeout=30)
            em = disnake.Embed(color=0x00ffff, title=word,
                               description="არის თუ არა ეს სიტყვა `არსებითი სახელი` ან `ზედსართავი სახელი?`")


            old = await inter.followup.send(embed=em, view=button, delete_after=40)

            if await button.wait():
                break

            match button.choice:
                case None:
                    continue
                case False:
                    await self.client.db.verify_word(word, 0)
                    earned += 5
                case True:
                    await self.client.db.verify_word(word, 1)
                    earned += 10

            await old.delete()

        user = await self.client.db.users.get(inter.author.id)
        user.wallet += earned
        await self.client.db.users.update(user)

        em = disnake.Embed(color=0x00ff00, description=f"შენ გამოიმუშავე: {earned}")
        await inter.followup.send(embed=em)






def setup(client: Client):
    client.add_cog(GeoWordleGame(client))
