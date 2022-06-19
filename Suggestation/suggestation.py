from redbot.core import commands

class Suggestation(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def suggest(self, ctx, suggestion):
        """This does stuff!"""
        # Your code will go here
        await ctx.send("I can do stuff!" + suggestion)

