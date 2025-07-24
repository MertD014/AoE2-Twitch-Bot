import json
from twitchio.ext import commands

class Info(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        with open("data/data.json") as f:
            self.data = json.load(f)

    @commands.command(name="civ")
    async def civ(self, ctx: commands.Context, *, civ_name: str):
        """Provides information about a specific civilization."""
        civ_name = civ_name.lower()
        for civ_data in self.data["civs"]:
            if civ_data["name"].lower() == civ_name:
                await ctx.send(f"{civ_data['name']}: {civ_data['team_bonus']}")
                return
        await ctx.send(f"Civilization '{civ_name}' not found.")

    @commands.command(name="unit")
    async def unit(self, ctx: commands.Context, *, unit_name: str):
        """Provides information about a specific unit."""
        unit_name = unit_name.lower()
        for unit_data in self.data["units"]:
            if unit_data["name"].lower() == unit_name:
                await ctx.send(f"{unit_data['name']}: {unit_data['description']}")
                return
        await ctx.send(f"Unit '{unit_name}' not found.")

    @commands.command(name="tech")
    async def tech(self, ctx: commands.Context, *, tech_name: str):
        """Provides information about a specific technology."""
        tech_name = tech_name.lower()
        for tech_data in self.data["techs"]:
            if tech_data["name"].lower() == tech_name:
                await ctx.send(f"{tech_data['name']}: {tech_data['description']}")
                return
        await ctx.send(f"Technology '{tech_name}' not found.")

def prepare(bot: commands.Bot):
    bot.add_cog(Info(bot))
