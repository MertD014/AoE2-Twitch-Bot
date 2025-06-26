import os
import aiohttp
import asyncpg
from twitchio.ext import commands

# --- Environment Variables ---
AOE2_ID = os.environ.get("AOE2_ID")
DATABASE_URL = os.environ.get("DATABASE_URL")

class AoE2(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.pool = None
        self.bot.loop.create_task(self._init_db())

    # --- Database Helper Methods ---
    async def _init_db(self):
        """
        Initializes the database connection pool and creates the score table if it doesn't exist. Run on init.
        """
        if not DATABASE_URL:
            print("CRITICAL: DATABASE_URL is not configured. Score commands will not work.")
            return

        try:
            self.pool = await asyncpg.create_pool(dsn=DATABASE_URL, min_size=1, max_size=5)
            async with self.pool.acquire() as con:
                await con.execute('''
                    CREATE TABLE IF NOT EXISTS score (
                        channel_name TEXT PRIMARY KEY,
                        wins INTEGER NOT NULL DEFAULT 0,
                        losses INTEGER NOT NULL DEFAULT 0
                    )
                ''')
            print("Successfully connected to PostgreSQL and ensured score aaaaq exists.")
        except Exception as e:
            print(f"Error: Could not connect to PostgreSQL database: {e}")
            self.pool = None

    async def _get_score(self, channel_name: str) -> tuple[int, int]:
        """Fetches the current score for a given channel from the database."""
        if not self.pool:
            return (0, 0)
        
        async with self.pool.acquire() as con:
            record = await con.fetchrow("SELECT wins, losses FROM score WHERE channel_name = $1", channel_name)
            if record:
                return record['wins'], record['losses']
            return (0, 0)

    async def _update_score(self, channel_name: str, wins: int, losses: int):
        """Saves or updates the score for a given channel in the database."""
        if not self.pool:
            return

        async with self.pool.acquire() as con:
            await con.execute("""
                INSERT INTO score (channel_name, wins, losses)
                VALUES ($1, $2, $3)
                ON CONFLICT (channel_name) DO UPDATE
                SET wins = EXCLUDED.wins, losses = EXCLUDED.losses
            """, channel_name, wins, losses)

    # --- Data Fetching Method ---
            
    async def _fetch_data_async(self, session: aiohttp.ClientSession, url: str) -> dict:
        """This asynchronous function fetches and returns JSON data using aiohttp."""
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        async with session.get(url, headers=headers) as response:
            response.raise_for_status()
            return await response.json()

    # --- Commands ---

    @commands.command(name="elo")
    async def elo(self, ctx: commands.Context):
        """Fetches and displays your current AoE2 ELO and stats from aoe2recs.com."""
        if not AOE2_ID:
            await ctx.send("The AOE2_ID (profile ID) is not configured in the bot's environment.")
            return

        url = f"https://aoe2recs.com/dashboard/api/profile?uid={AOE2_ID}"

        try:
            async with aiohttp.ClientSession() as session:
                data = await self._fetch_data_async(session, url)
            
            solo_elo = data.get('mmr_rm_1v1', 'N/A')
            team_elo = data.get('mmr_rm_tg', 'N/A')
            await ctx.send(f"RM 1v1: {solo_elo} | RM Team: {team_elo}")

        except aiohttp.ClientResponseError as e:
            await ctx.send(f"An HTTP error occurred. The API might be down. (Error: {e.status})")
        except Exception as e:
            await ctx.send("An unexpected error occurred while fetching ELO.")
            print(f"An error occurred in the elo command: {e}")

    @commands.command(name="rank")
    async def elo(self, ctx: commands.Context):
        """Fetches and displays your current AoE2 rank and stats from aoe2recs.com."""
        if not AOE2_ID:
            await ctx.send("The AOE2_ID (profile ID) is not configured in the bot's environment.")
            return

        url = f"https://aoe2recs.com/dashboard/api/profile?uid={AOE2_ID}"

        try:
            async with aiohttp.ClientSession() as session:
                data = await self._fetch_data_async(session, url)
            
            solo_rank = data.get('rank_rm_1v1', 'N/A')
            team_rank = data.get('ramk_rm_tg', 'N/A')
            await ctx.send(f"RM 1v1: {solo_rank} | RM Team: {team_rank}")

        except aiohttp.ClientResponseError as e:
            await ctx.send(f"An HTTP error occurred. The API might be down. (Error: {e.status})")
        except Exception as e:
            await ctx.send("An unexpected error occurred while fetching ELO.")
            print(f"An error occurred in the elo command: {e}")
            
    @commands.command(name="score")
    async def score(self, ctx: commands.Context, *, action: str = None):
        """
        Manages the session score, stored persistently in a database.
        Usage: !score | !score win | !score loss | !score reset
        """
        if not self.pool:
            await ctx.send("Database connection is not available. Please check the bot logs.")
            return
            
        channel = ctx.channel.name
        wins, losses = await self._get_score(channel)

        if action is None:
            await ctx.send(f"Current score: {wins} Wins / {losses} Losses")
            return

        action = action.lower()

        if not ctx.author.is_mod:
            await ctx.send("Sorry, only moderators can change the score.")
            return

        if action in ["win", "w"]:
            wins += 1
            await self._update_score(channel, wins, losses)
            await ctx.send(f"Win recorded! New score: {wins} Wins / {losses} Losses")
        
        elif action in ["loss", "l"]:
            losses += 1
            await self._update_score(channel, wins, losses)
            await ctx.send(f"Loss recorded. New score: {wins} Wins / {losses} Losses")

        elif action == "reset":
            wins, losses = 0, 0
            await self._update_score(channel, wins, losses)
            await ctx.send("Score has been reset to 0 Wins / 0 Losses.")
        
        else:
            await ctx.send(f"Unknown action '{action}'. Please use win, loss, or reset.")

def prepare(bot: commands.Bot):
    """Adds the AoE2 cog to the bot."""
    bot.add_cog(AoE2(bot))