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
        # Your code will go here
        #await self.config.guild(557986764548079617).channel(800328370252415006)

        channel = get(ctx.guild.text_channels, 800328370252415006)
        server = ctx.guild.id
        msg = await channel.send(content=suggestion, embed=embed)

        #await client.get_guild(557986764548079617).get_channel(800328370252415006).send(suggestion)
        #await ctx.send("I can do stuff!" + suggestion)
