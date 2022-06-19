from discord import client
from redbot.core import commands

class Suggestation(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def suggest(self, ctx, suggestion):
        """This does stuff!"""
        # Your code will go here
        await self.config.guild(557986764548079617).channel(800328370252415006)

        #await client.get_guild(557986764548079617).get_channel(800328370252415006).send(suggestion)
        await ctx.send("I can do stuff!" + suggestion)
