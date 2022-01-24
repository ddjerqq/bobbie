import discord
from discord.ext import commands

import app


class Connection(commands.Cog):

    def __init__(self, app):
        self.app = app

    @commands.Cog.listener()
    async def on_ready(self):
        print("Bobbie succesfully connected.")
        activity = discord.Game("discord.gg/georgia")
        status = discord.Status.dnd
        await app.app.change_presence(activity=activity, status=status)

    @commands.command()
    async def post_rules(self, ctx):
        embed = discord.Embed(title="Bobbie's Campfire",
                              description="Bobbie's Campfire არის ერთ ერთი ქართული დისქორდ სერვერი სხვადასხვა თემებზე დისკუსიებისთვის.",
                              color=0x2d56a9)
        embed.add_field(name="1. სპამი / ფლუდი",
                        value="პირველი და მთავარი სერვერის წესი - არასოდეს გასპამოთ / გაფლუდოთ სერვერის მთავარი სასაუბრო არხი - #general .",
                        inline=False)
        embed.add_field(name="2. ავადმყოფური თემები",
                        value="ისე თემებზე საუბარი როგორიცაა პედოფილია, გაუპატიურება და ასე შემდეგ, სასტიკად აკრძალულია ჩვენს დისქორდზე. თუ ჩეამჩნიეთ რომ ვირმე არღვევს ამ წესს, დაუკავშირდეთ staff წევრს.",
                        inline=False)
        embed.add_field(name="3. შეურაცხყოფა",
                        value="სხვა წევრების საჯაროდ შეურაცხყოფა აკრძალულია. პირადში რაც მოხდება, სერვერი არ არის პასუხისმგებელი.",
                        inline=False)
        embed.add_field(name="4. დოქსინგი", value="გთხოვთ, არ გაავრცელოთ სხვა წევრების პირადული ცხოვრების ინფორმაცია.",
                        inline=False)
        embed.add_field(name="5. რეკლამა", value="სხვა სერვერების / საიტების რეკლამირება აკრძალულია.", inline=False)
        embed.add_field(name="6. კამათი Staff წევრებთან",
                        value="ჩვენი staff წევრების ერთადერთი მიზანია რომ ყველა გაერთოს და თავი კარგად იგრძნოს ჩვენს სერვერზე. თუ staff წევრის ზომით არ ხართ კმაყოფილი, დაუკავშირდით პირადში. ღია ჩატში მიღებულ ზომაზე კამათი აკრძალულია.",
                        inline=False)
        embed.add_field(name="7. Discord ToS",
                        value="წევრები არიან ვალდებულნი პატივი სცენ დისქორდის ToS, თუ დავინახეთ რომ რომელიმე წევრი არღვევს მას, მივიღებთ ზომებს გაფრთხილების გარეშე და ასევე დავარეპორტებთ Discord მოდერაციასთან.",
                        inline=True)
        embed.set_footer(
            text="Bobbie Bot - სპეციალურად Bobbie's Campfire სერვერისთვის. წესები შეიძლება შეიცვალოს ნებისმიერ დროს, ადევნეთ თვალი.")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/934320061563408445/934381795611406336/logo.jpg")
        await ctx.send(embed=embed)

def setup(app):
    app.add_cog(Connection(app))
