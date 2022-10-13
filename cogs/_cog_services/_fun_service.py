import random

import disnake
from disnake import ApplicationCommandInteraction as Aci
from disnake.ext import commands

from client.client import Client
from database import ItemType
from database.factories.marriage_factory import MarriageFactory


class FunService:
    def __init__(self, client: Client):
        self.__client = client

    def gay(self, sender: disnake.Member, target: disnake.Member) -> disnake.Embed:
        em = disnake.Embed(
            title="გეი ჰორმონების პროცენტის გამოცნობის მექანიზმი",
            color=0x2d56a9)

        em.add_field(
            name="გეი ტესტის რეზულტატი",
            value=f"{sender.mention}'მ ჩაიტარა გეი გამოკვლების ტესტი და აღმოაჩინა რომ {target.mention} "
                  f"{random.randint(1, 100)} პროცენთით გეია 🏳️‍🌈.")

        return em

    def slap(self, user: disnake.Member, target: disnake.Member) -> disnake.Embed:
        em = disnake.Embed(
            color=0x2d56a9,
            description=f"{user.mention} გაბრაზდა და ძლიერად შემოულაწუნა {target.mention}'ს ✊"
        )
        return em

    def hug(self, user: disnake.Member, target: disnake.Member) -> disnake.Embed:
        em = disnake.Embed(
            color=0x2d56a9,
            description=f"{user.mention} გულიანად ჩაეხუტა {target.mention}'ს <3"
        )
        return em

    def kiss(self, user: disnake.Member, target: disnake.Member) -> disnake.Embed:
        em = disnake.Embed(
            color=0x2d56a9,
            description=f"{user.mention}'მ აკოცა {target.mention}'ს <3"
        )
        return em

    def coffee(self, user: disnake.Member) -> disnake.Embed:
        coffee_types = [
            "კაპუჩინო",
            "მოკა",
            "ბობა"
        ]
        em = self.__client.embeds.generic.generic_success(
            title=f"{user.name}'მ დალია {random.choice(coffee_types)} ყავა",
        )
        return em

    def tea(self, user: disnake.Member) -> disnake.Embed:
        tea_types = [
            "მწვანე",
            "შავი",
            "ტყის",
            "კენკრის",
            "მოცვის",
            "მოცოცვის"
        ]
        em = self.__client.embeds.generic.generic_success(
            title=f"{user.name}'მ დალია {random.choice(tea_types)} ჩაი",
        )

        return em

    def beer(self, user: disnake.Member) -> disnake.Embed:
        beer_types = [
            "ბავარიული",
            "შავი",
            "ავსტრიული",
            "ჩამოსასხმელი",
            "ნატახტარის",
            "ზედაზენის"
        ]
        em = self.__client.embeds.generic.generic_success(
            title=f"{user.name}'მ დალია {random.choice(beer_types)} ლუდი"
        )

        return em

    def popcorn(self, user: disnake.Member) -> disnake.Embed:
        em = self.__client.embeds.generic.generic_success(
            title=f"{user.name}'მ საიდანღაც დააძრო პოპკორნი"
        )
        return em

    def fuck(self, user: disnake.Member, target: disnake.Member) -> disnake.Embed:
        em = disnake.Embed(
            color=0x2d56a9,
            description=f"{user.mention}'მ მაგრად მოტყნა {target.mention}"
        )
        return em
