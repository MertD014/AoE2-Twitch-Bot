import os
from twitchio.ext import commands

DISCORD_LINK= os.environ.get("DISCORD_LINK")

class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        await ctx.send("Pong!")

    @commands.command(name="discord", aliases=["dc"])
    async def discord(self, ctx: commands.Context):
        await ctx.send(f"You will need roles for full access! {DISCORD_LINK}")

    @commands.command(name="game")
    async def game(self, ctx: commands.Context):
        """Displays the current game being played on the stream."""
        try:
            streams = await self.bot.fetch_streams(user_logins=[ctx.channel.name])

            if streams:
                stream_info = streams[0]
                game_name = stream_info.game_name
                await ctx.send(f"We're currently playing: {game_name}!")
            else:
                await ctx.send("The stream is currently offline.")
        except Exception as e:
            await ctx.send("Sorry, I couldn't fetch the current game information at the moment.")
            print(f"Error in !game command: {e}")
    
    @commands.command(name="help")
    async def help(self, ctx: commands.Context):
        """Sends a whisper to the user with a list of all available commands."""
        command_names = [f"!{cmd.name}" for cmd in self.bot.commands.values()]
        command_names.sort()
        help_message = f"Hello! Here are the commands you can use: {', '.join(command_names)}"

        try:
            await ctx.author.send(help_message)
            await ctx.send(f"@{ctx.author.name}, I've sent you a whisper with a list of my commands! 📬")
        except Exception as e:
            await ctx.send(f"@{ctx.author.name}, I couldn't send you a whisper. Please make sure you have whispers enabled from strangers.")
            print(f"Error in !help command (could not send whisper): {e}")

def prepare(bot: commands.Bot):
    bot.add_cog(General(bot))