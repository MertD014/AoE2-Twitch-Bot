from twitchio.ext import commands

class Minecraft(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ip")
    async def ip_command(self, ctx: commands.Context):
        """Provides information about how to join the Minecraft server."""         
        await ctx.send("I'm currently playing on a private Minecraft Realms server! I love adding regulars from our community to the whitelist, so the best way to get an invite is to hang out and be active in chat. 😊")

    @commands.command(name="seed")
    async def seed(self,ctx: commands.Context):
        await ctx.send("Use seed 'sid' to play the same map!")

    @commands.command(name="version")
    async def version(self,ctx: commands.Context):
        await ctx.send("I play on 1.21.6!")
    
    #add seed command

def prepare(bot: commands.Bot):
    bot.add_cog(Minecraft(bot))