import discord
import json
import requests as r
from random import randint
from discord.ext import commands


class Commands(commands.Cog, commands.Bot):

    def __init(self, app):
        self.app = app

    @commands.command()
    # @commands.cooldown(1, 30, commands.BucketType.user)
    async def gay(self, ctx):
        content = ctx.message.content
        process = str(content).replace("!gay", "").strip()
        embed = discord.Embed(title="გეი ჰორმონების პროცენტის გამოცნობის მექანიზმი", color=0x2d56a9)
        random = randint(1, 100)
        embed.add_field(name="ტესტის რეზულტატი".format(ctx.message.author.mention),
                        value="{0}'მ გატესტა მექანიზმი და აღმოაჩინა რომ {1} {2} პროცენტით გეია 🏳️‍🌈.".format(
                            ctx.message.author.mention, process, random), inline=False)
        if not process:
            await ctx.send("ვინმე დაპინგე!")
        else:
            await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.command()
    # @commands.cooldown(1, 30, commands.BucketType.user)
    async def coffee(self, ctx, member: discord.Member = None):
        member = member.mention
        content = ctx.message.content
        process = str(content).replace("!coffee", "").strip()
        if not process:
            await ctx.send("ვინმე დაპინგე!")
        else:
            await ctx.send("%s დაპატიჟა ყავაზე %s ☕" % (ctx.message.author.mention, member))
        await ctx.message.delete()

    @commands.command()
    # @commands.cooldown(1, 30, commands.BucketType.user)
    async def tea(self, ctx, member: discord.Member = None):
        member = member.mention
        content = ctx.message.content
        process = str(content).replace("!tea", "").strip()
        if not process:
            await ctx.send("ვინმე დაპინგე!")
        else:
            await ctx.send("%s შესთავაზა ჩაი %s ☕" % (ctx.message.author.mention, member))
        await ctx.message.delete()

    @commands.command()
    # @commands.cooldown(1, 30, commands.BucketType.user)
    async def hug(self, ctx, member: discord.Member = None):
        member = member.mention
        content = ctx.message.content
        process = str(content).replace("!hug", "").strip()
        if not process:
            await ctx.send("ვინმე დაპინგე!")
        else:
            await ctx.send("%s გულიანად ჩაეხუტა %s'ს🫂" % (ctx.message.author.mention, member))
        await ctx.message.delete()

    @commands.command()
    # @commands.cooldown(1, 30, commands.BucketType.user)
    async def fuck(self, ctx, member: discord.Member = None):
        random = randint(1, 100)
        member = member.mention
        content = ctx.message.content
        process = str(content).replace("!fuck", "").strip()
        if not process:
            await ctx.send("ვინმე დაპინგე მოსატყნავად!!")
        elif random < 50:
            await ctx.send("%s აუდგა და შეეცადა %s გაჟიმვას, მარა როგორც კი შეუდო ეგრევე გული წაუვიდა." % (ctx.message.author, member))
        elif random > 50:
            await ctx.send("%s აუდგა და გულიანად და ღრმად გაჟიმა %s 😎" % (ctx.message.author, member))
        else:
            # await ctx.send("%s გაჟიმა %s 😎" % (ctx.message.author.mention, member))
            pass

        await ctx.message.delete()

    @commands.command()
    async def post_rules(self, ctx):
        embed = discord.Embed(title="Frosty's Campfire",
                              description="Frosty's Campfire არის ერთ ერთი ქართული დისქორდ სერვერი სხვადასხვა თემებზე დისკუსიებისთვის.",
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
            text="Bobbie - სპეციალურად Frosty's Campfire სერვერისთვის. წესები შეიძლება შეიცვალოს ნებისმიერ დროს, ადევნეთ თვალი.")
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/934320061563408445/934381795611406336/logo.jpg")
        await ctx.send(embed=embed)


def setup(app):
    app.add_cog(Commands(app))
