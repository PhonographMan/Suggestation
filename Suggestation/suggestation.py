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
        embed = discord.Embed(color=await ctx.embed_colour(), description="This is a description")

        channel = get(ctx.guild.text_channels, id=800328370252415006)
        msg = await channel.send(content=suggestion, embed=embed)
