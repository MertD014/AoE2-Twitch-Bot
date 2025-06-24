import os
from twitchio.ext import commands

DISCORD_LINK= os.environ.get("DISCORD_LINK");

class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        await ctx.send("Pong!")

    @commands.command(name="discord", aliases=["dc"])
    async def discord(self, ctx: commands.Context):
        await ctx.send(f"You will need roles for full access! {DISCORD_LINK}")

def prepare(bot: commands.Bot):
    bot.add_cog(General(bot))