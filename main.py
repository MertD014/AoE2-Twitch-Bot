import os
import json
from twitchio.ext import commands
from dotenv import load_dotenv

load_dotenv()

# --- Configuration ---
TWITCH_TOKEN = os.environ.get("ACCESS_TOKEN")
CHANNEL = os.environ.get("CHANNEL_NAME")
PREFIX = "!"

INITIAL_COGS = [
    "cogs.general",
    "cogs.aoe2",
    "cogs.fun",
]

class Bot(commands.Bot):
    def __init__(self, client_id, client_secret, bot_id):
        super().__init__(
            token=TWITCH_TOKEN,
            prefix=PREFIX,
            initial_channels=[CHANNEL],
            client_id=client_id,
            client_secret=client_secret
        )
        self.data = self._load_data()
        for cog in INITIAL_COGS:
            try:
                self.load_module(cog)
                print(f"Successfully loaded cog: {cog}")
            except Exception as e:
                print(f"Failed to load cog {cog}: {e}")

    def _load_data(self):
        """Loads data from the data.json file."""
        try:
            with open("data/data.json", "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print("Error: data.json not found.")
            return {}
        except json.JSONDecodeError:
            print("Error: Could not decode data.json.")
            return {}

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

if __name__ == "__main__":
    CLIENT_ID = os.environ.get("CLIENT_ID")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
    BOT_ID = os.environ.get("BOT_ID")

    if not all([TWITCH_TOKEN, CLIENT_ID, CLIENT_SECRET, BOT_ID]):
        print("CRITICAL Error: Missing one or more required environment variables.")
    elif not TWITCH_TOKEN.startswith("oauth:"):
        print("CRITICAL Error: ACCESS_TOKEN is invalid!")
    else:
        bot = Bot(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, bot_id=BOT_ID)
        bot.run()