import os
from twitchio.ext import commands

DISCORD_LINK= os.environ.get("DISCORD_LINK")

class General(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx: commands.Context):
        await ctx.send("Pong!")

    @commands.command(name="akkal")
    async def akkal(self, ctx: commands.Context):
        await ctx.send("3v3 League hosted by Akkal https://www.twitch.tv/akkalno")

    @commands.command(name="help")
    async def help(self, ctx: commands.Context):
        """Shows a list of all available commands."""
        command_names = [f"!{cmd.name}" for cmd in self.bot.commands.values()]
        command_names.sort()
        help_message = f"Hello! Here are the commands you can use: {', '.join(command_names)}"
        await ctx.send(help_message)

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
    async def help(self, ctx: commands.Context, command_name: str = None):
        """Shows a list of all commands, or details for a specific command."""

        if command_name is None:
            all_commands = sorted([f"!{cmd.name}" for cmd in self.bot.commands.values()])
            help_message = (
                f"Available Commands: {', '.join(all_commands)}. "
                "For more info, type !help <command_name> (e.g., !help score)"
            )
            await ctx.send(help_message)
            return

        command_name = command_name.lower().lstrip('!')
        command = self.bot.get_command(command_name)
        
        if command:
            name = f"!{command.name}"
            
            aliases = ""
            if command.aliases:
                aliases = f"(aliases: {', '.join(command.aliases)})"
            
            description = "No description available."
            
            if hasattr(command, '_callback') and command._callback.__doc__:
                description = command._callback.__doc__.strip().split('\n')[0]
                
            help_message = f"{name} {aliases} | {description}"
            await ctx.send(help_message)
            
        else:
            await ctx.send(f"Sorry, the command '!{command_name}' does not exist. Try !help to see all available commands.")

def prepare(bot: commands.Bot):
    bot.add_cog(General(bot))