from twitchio.ext import commands

class Minecraft(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ip")
    async def ip_command(self, ctx: commands.Context):
        """Provides information about how to join the Minecraft server."""         
        await ctx.send("I'm currently playing on a private Minecraft Realms server! I love adding regulars from our community to the whitelist, so the best way to get an invite is to hang out and be active in chat. 😊")

def prepare(bot: commands.Bot):
    bot.add_cog(Minecraft(bot))