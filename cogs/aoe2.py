import os
import requests
import json
from twitchio.ext import commands

AOE2_ID = os.environ.get("AOE2_ID")
SCORE_FILE = "../data/aoe2_score.json" 

class AoE2(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.wins = 0
        self.losses = 0
        self._load_score()

    # --- Helper Methods ---
    def _load_score(self):
        """Loads the score from the JSON file into memory."""
        try:
            if os.path.exists(SCORE_FILE):
                with open(SCORE_FILE, 'r') as f:
                    data = json.load(f)
                    self.wins = data.get('wins', 0)
                    self.losses = data.get('losses', 0)
        except Exception as e:
            print(f"Error loading score file: {e}")

    def _save_score(self):
        """Saves the current score from memory to the JSON file."""
        try:
            with open(SCORE_FILE, 'w') as f:
                data = {'wins': self.wins, 'losses': self.losses}
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error saving score file: {e}")

    # --- Data Fetching Method ---
    @staticmethod
    def _fetch_data_sync(url: str):
        """This synchronous function fetches and returns JSON data."""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()

    # --- !elo Command (with your changes) ---
    @commands.command(name="elo", aliases=["rank"])
    async def elo(self, ctx: commands.Context):
        """Fetches and displays your current AoE2 ELO and stats from aoe2recs.com."""
        if not AOE2_ID:
            await ctx.send("The AOE2_ID (profile ID) is not configured in the bot's environment.")
            return

        url = f"https://aoe2recs.com/dashboard/api/profile?uid={AOE2_ID}"
        loop = self.bot.loop

        try:
            data = await loop.run_in_executor(None, self._fetch_data_sync, url)
            solo_elo = data.get('mmr_rm_1v1', 'N/A')
            team_elo = data.get('mmr_rm_tg', 'N/A')
            # Using your simplified output string
            await ctx.send(f"RM 1v1: {solo_elo} | RM Team: {team_elo}")

        except requests.exceptions.HTTPError as e:
            await ctx.send(f"An HTTP error occurred. (Error: {e})")
        except Exception as e:
            await ctx.send("An unexpected error occurred.")
            print(f"An error occurred in the elo command: {e}")
            
    # --- !score Command ---
    @commands.command(name="score")
    async def score(self, ctx: commands.Context, *, action: str = None):
        """
        Manages the session score.
        Usage: !score | !score win | !score loss | !score reset
        """
        if action is None:
            await ctx.send(f"Current score since last reset: {self.wins} Wins / {self.losses} Losses")
            return

        action = action.lower()

        if not ctx.author.is_mod:
            await ctx.send("Sorry, only moderators can change the score.")
            return

        if action in ["win", "w"]:
            self.wins += 1
            self._save_score()
            await ctx.send(f"Win recorded! New score: {self.wins} Wins / {self.losses} Losses")
        
        # Case 3: Add a loss (!score loss)
        elif action in ["loss", "l"]:
            self.losses += 1
            self._save_score()
            await ctx.send(f"Loss recorded. New score: {self.wins} Wins / {self.losses} Losses")

        # Case 4: Reset the score (!score reset)
        elif action == "reset":
            self.wins = 0
            self.losses = 0
            self._save_score()
            await ctx.send("Score has been reset to 0 Wins / 0 Losses.")
        
        # Case 5: Handle unknown actions
        else:
            await ctx.send(f"Unknown action '{action}'. Please use win, loss, or reset.")

def prepare(bot: commands.Bot):
    bot.add_cog(AoE2(bot))