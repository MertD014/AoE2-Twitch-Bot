import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from twitchio.ext import commands

class SpotifyCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spotify = self._setup_spotify()

    def _setup_spotify(self):
        scope = "user-read-currently-playing"
        auth_manager = SpotifyOAuth(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
            scope=scope,
        )
        return spotipy.Spotify(auth_manager=auth_manager)

    @commands.command(name="song")
    async def song_command(self, ctx):
        """Displays the currently playing song on Spotify."""
        current_track = self.spotify.current_user_playing_track()
        if current_track and current_track['is_playing']:
            artist = current_track['item']['artists'][0]['name']
            song_title = current_track['item']['name']
            await ctx.send(f"Currently playing: {song_title} by {artist}")
        else:
            await ctx.send("Not currently playing any song on Spotify.")

def prepare(bot):
    bot.add_cog(SpotifyCog(bot))
