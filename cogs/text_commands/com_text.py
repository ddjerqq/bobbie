import disnake
from random import randint
from disnake.ext import commands


class BobbiCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    # @commands.cooldown(1, 30, commands.BucketType.user)
    async def gay(self, ctx, target: disnake.Member = None):
        embed = disnake.Embed(title="გეი ჰორმონების პროცენტის გამოცნობის მექანიზმი", color=0x2d56a9)
        random = randint(1, 100)
        if target is None or target == ctx.message.author:
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

    @commands.command()
    # @commands.cooldown(1, 30, commands.BucketType.user)
    async def coffee(self, ctx, target: disnake.Member = None):
        if target is None or target == ctx.message.author:
            await ctx.send("%s'მა დაისხა ყავა თავისთვის ☕" % ctx.message.author.mention)
        else:
            await ctx.send("%s დაპატიჟა ყავაზე %s ☕" % (ctx.message.author.mention, target.mention))

    @commands.command()
    # @commands.cooldown(1, 30, commands.BucketType.user)
    async def tea(self, ctx, target: disnake.Member = None):
        if target is None or target == ctx.message.author:
            await ctx.send("%s'მა დაისხა ჩაი თავისთვის ☕" % ctx.message.author.mention)
        else:
            await ctx.send("%s შესთავაზა ჩაი %s ☕" % (ctx.message.author.mention, target.mention))

    @commands.command()
    # @commands.cooldown(1, 30, commands.BucketType.user)
    async def hug(self, ctx, target: disnake.Member = None):
        if target is None or target == ctx.message.author:
            await ctx.send("%s'მ მოიწყინა და დაუწყო თავის თავს მოფერება 🫂" % ctx.message.author.mention)
        else:
            await ctx.send("%s გულიანად ჩაეხუტა %s'ს🫂" % (ctx.message.author.mention, target.mention))

    @commands.command()
    # @commands.cooldown(1, 30, commands.BucketType.user)
    async def slap(self, ctx, target: disnake.Member = None):
        if target is None or target == ctx.message.author:
            await ctx.send("%s გააფრინა და თავის თავს გიჟივით დაუწყო ცემა ✊" % ctx.message.author.mention)
        else:
            await ctx.send("%s გაბრაზდა და ძლიერად შემოულაწუნა %s ✊" % (ctx.message.author.mention, target.mention))

    @commands.command()
    # @commands.cooldown(1, 30, commands.BucketType.user)
    async def popcorn(self, ctx, target: disnake.Member = None):
        if target is None or target == ctx.message.author:
            await ctx.send("%s დაინტრიგდა სიტუაციით,მოხალა პოპკორნი და ჩაუჯდა ჩათს 🍿" % ctx.message.author.mention)
        else:
            await ctx.send("%s გააძრო საიდანღაც პოპკორნი, არ მკითხო როგორ, და შესთავაზა %s 🍿" % (ctx.message.author.mention, target.mention))

    @commands.command()
    # @commands.cooldown(1, 30, commands.BucketType.user)
    async def beer(self, ctx, target: disnake.Member = None):
        if target is None or target == ctx.message.author:
            await ctx.send("%s'მ დაისხა ლუდი და მოწრუპა ჭიქიდან, შემდეგ კი ჩაცალა მთლიანი ბოთლი როგორც ნამდვილმა "
                           "ლოთმა 🍺" % ctx.message.author.mention)
        else:
            await ctx.send("%s'მ დაისხა ლუდი თავისთვის და ასევე დაუსხა %s 🍻" % (ctx.message.author.mention, target.mention))

def setup(client):
    client.add_cog(BobbiCommands(client))
