import os
from twitchio.ext import commands
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
TWITCH_TOKEN = os.environ.get("ACCESS_TOKEN")
CHANNEL = os.environ.get("CHANNEL_NAME")
PREFIX = "!"

# --- List of cogs to load ---
INITIAL_COGS = [
    "cogs.general",
    "cogs.aoe2",
    "cogs.minecraft",
    "cogs.fun",
    "cogs.info"
]

# --- Main Bot Class ---
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            token=TWITCH_TOKEN,
            prefix=PREFIX,
            initial_channels=[CHANNEL]
        )

    def setup_cogs(self):
        """Loads the initial cogs."""
        for cog in INITIAL_COGS:
            try:
                self.load_module(cog)
                print(f"Successfully loaded cog: {cog}")
            except Exception as e:
                print(f"Failed to load cog {cog}: {e}")

    async def event_ready(self):
        """Called once when the bot goes online."""
        print(f"Logged in as | {self.nick}")
        if self.connected_channels:
            channel_names = [channel.name for channel in self.connected_channels]
            print(f"Joining channels | {', '.join(channel_names)}")
        else:
            print("No initial channels specified or failed to join.")
        print("-" * 20)

    async def event_message(self, message):
        """Runs every time a message is sent in chat."""
        if message.echo:
            return
        await self.handle_commands(message)   

# --- Main ---
if __name__ == "__main__":
    if not TWITCH_TOKEN or not TWITCH_TOKEN.startswith("oauth:"):
        print("CRITICAL Error: ACCESS_TOKEN is missing or invalid!")
    else:
        bot = Bot()
        bot.setup_cogs()
        bot.run()