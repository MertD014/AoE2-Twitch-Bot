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
        for civ, civ_id in self.data["civ_names"].items():
            if civ.lower() == civ_name:
                civ_info = self.data["civ_helptexts"][civ_id]
                await ctx.send(f"{civ}: {civ_info}")
                return
        await ctx.send(f"Civilization '{civ_name}' not found.")

    @commands.command(name="unit")
    async def unit(self, ctx: commands.Context, *, unit_name: str):
        """Provides information about a specific unit."""
        unit_name = unit_name.lower()
        for unit, unit_id in self.data["unit_names"].items():
            if unit.lower() == unit_name:
                unit_info = self.data["unit_helptexts"][unit_id]
                await ctx.send(f"{unit}: {unit_info}")
                return
        await ctx.send(f"Unit '{unit_name}' not found.")

    @commands.command(name="tech")
    async def tech(self, ctx: commands.Context, *, tech_name: str):
        """Provides information about a specific technology."""
        tech_name = tech_name.lower()
        for tech, tech_id in self.data["tech_names"].items():
            if tech.lower() == tech_name:
                tech_info = self.data["tech_helptexts"][tech_id]
                await ctx.send(f"{tech}: {tech_info}")
                return
        await ctx.send(f"Technology '{tech_name}' not found.")

def prepare(bot: commands.Bot):
    bot.add_cog(Info(bot))
