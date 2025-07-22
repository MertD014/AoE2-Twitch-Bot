import os
import datetime
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
        """Shows a list of all available commands."""
        # TODO: Replace with a link to a commands page
        command_names = [f"!{cmd.name}" for cmd in self.bot.commands.values()]
        command_names.sort()
        help_message = f"Hello! Here are the commands you can use: {', '.join(command_names)}"
        await ctx.send(help_message)

    @commands.command(name="uptime")
    async def uptime(self, ctx: commands.Context):
        """Shows how long the stream has been live."""
        try:
            streams = await self.bot.fetch_streams(user_logins=[ctx.channel.name])
            if streams:
                stream_info = streams[0]
                started_at = stream_info.started_at
                uptime = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc) - started_at

                # Format the uptime into a human-readable string
                hours, remainder = divmod(int(uptime.total_seconds()), 3600)
                minutes, seconds = divmod(remainder, 60)

                if hours > 0:
                    await ctx.send(f"The stream has been live for {hours} hours and {minutes} minutes.")
                elif minutes > 0:
                    await ctx.send(f"The stream has been live for {minutes} minutes and {seconds} seconds.")
                else:
                    await ctx.send(f"The stream has been live for {seconds} seconds.")
            else:
                await ctx.send("The stream is currently offline.")
        except Exception as e:
            await ctx.send("Sorry, I couldn't fetch the stream uptime at the moment.")
            print(f"Error in !uptime command: {e}")

def prepare(bot: commands.Bot):
    bot.add_cog(General(bot))