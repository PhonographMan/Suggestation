import discord
from discord import client
from discord.utils import get
from redbot.core import commands
from redbot.core.utils import embed


class Suggestation(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def suggest(self, ctx, suggestion):
        """This does stuff!"""
        embed = discord.Embed(
            title="Suggestion",
            #color=await ctx.embed_colour(),
            color=await discord.Color("#F0F000"),
            description="Special Heads for the months of May/June given out to recent graduates to celebrate our Dominionites RL Accomplishment"
        )

        embed.add_field(name="IS YOUR IDEA AN EXISTING PLUGIN OR DATAPACK?", value=f"no", inline=False)
        embed.add_field(name="WHY SHOULD WE ADD THIS SUGGESTION?", value=f"I think it would be a fun way to celebrate members of our community as that's a major life event for many people. We have a lot of younger people on the server and it would be a nice way to show some support.", inline=False)
        embed.add_field(name="ANY OTHER USEFUL INFORMATION", value=f"Just an addition for community spirit", inline=False)

        channel = get(ctx.guild.text_channels, id=800328370252415006)
        msg = await channel.send("", embed=embed)
