import random
from twitchio.ext import commands

class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="dice")
    async def dice(self, ctx: commands.Context, num_sides: int = 6):
        """Rolls a dice with a specified number of sides."""
        if num_sides <= 0:
            await ctx.send("The number of sides must be a positive number.")
            return
        roll = random.randint(1, num_sides)
        await ctx.send(f"{ctx.author.name} rolled a {roll}!")

    @commands.command(name="coin")
    async def coin(self, ctx: commands.Context):
        """Flips a coin to your witcher friend"""
        flip = random.randint(1,2)
        if flip:
            await ctx.send("Heads!")
        else:
            await ctx.send("Tails!")

def prepare(bot: commands.Bot):
    """Adds the Fun cog to the bot."""
    bot.add_cog(Fun(bot))

