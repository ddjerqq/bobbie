import discord
from random import randint
from discord.ext import commands


class Commands(commands.Cog, commands.Bot):

    def __init(self, app):
        self.app = app

    @commands.command()
    # @commands.cooldown(1, 30, commands.BucketType.user)
    async def gay(self, ctx, target: discord.Member = None):
        embed = discord.Embed(title="გეი ჰორმონების პროცენტის გამოცნობის მექანიზმი", color=0x2d56a9)
        random = randint(1, 100)
        if target is None or target == ctx.message.author:
            print("same author detected")
            embed.add_field(name="გეი ტესტის რეზულტატი",
                            value="{0}'მ ჩაიტარა გეი გამოკვლების ტესტი და აღმოაჩინა რომ {1} პროცენთით გეია 🏳️‍🌈.".format(
                                ctx.message.author.mention, random), inline=False)
            await ctx.send(embed=embed)
        else:
            target_mention = target.mention
            embed.add_field(name="გეი ტესტის რეზულტატი",
                            value="{0}'მ გატესტა მექანიზმი და აღმოაჩინა რომ {1} {2} პროცენტით გეია 🏳️‍🌈".format(
                                ctx.message.author.mention, target_mention, random), inline=False)
            await ctx.send(embed=embed)
        await ctx.message.delete()

    @commands.command()
    # @commands.cooldown(1, 30, commands.BucketType.user)
    async def coffee(self, ctx, target: discord.Member = None):
        if target is None or target == ctx.message.author:
            await ctx.send("%s'მა დაისხა ყავა თავისთვის ☕" % ctx.message.author.mention)
        else:
            await ctx.send("%s დაპატიჟა ყავაზე %s ☕" % (ctx.message.author.mention, target.mention))
        await ctx.message.delete()

    @commands.command()
    # @commands.cooldown(1, 30, commands.BucketType.user)
    async def tea(self, ctx, target: discord.Member = None):
        if target is None or target == ctx.message.author:
            await ctx.send("%s'მა დაისხა ჩაი თავისთვის ☕" % ctx.message.author.mention)
        else:
            await ctx.send("%s შესთავაზა ჩაი %s ☕" % (ctx.message.author.mention, target.mention))
        await ctx.message.delete()

    @commands.command()
    # @commands.cooldown(1, 30, commands.BucketType.user)
    async def hug(self, ctx, target: discord.Member = None):
        if target is None or target == ctx.message.author:
            await ctx.send("%s'მ მოიწყინა და დაუწყო თავის თავს მოფერება 🫂" % ctx.message.author.mention)
        else:
            await ctx.send("%s გულიანად ჩაეხუტა %s'ს🫂" % (ctx.message.author.mention, target.mention))
        await ctx.message.delete()

    @commands.command()
    # @commands.cooldown(1, 30, commands.BucketType.user)
    async def beer(self, ctx, target: discord.Member = None):
        if target is None or target == ctx.message.author:
            await ctx.send("%s'მ დაისხა ლუდი და მოწრუპა ჭიქიდან, შემდეგ კი ჩაცალა მთლიანი ბოთლი როგორც ნამდვილმა "
                           "ლოთმა 🍺" % ctx.message.author.mention)
        else:
            await ctx.send("%s'მ დაისხა ლუდი თავისთვის და ასევე დაუსხა %s 🍻" % (ctx.message.author.mention, target.mention))
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
