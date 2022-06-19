import discord
from discord import client
from discord.utils import get
from redbot.core import commands
from redbot.core.utils import embed
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.predicates import ReactionPredicate


class Suggestation(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def suggest(self, ctx, suggestion):
        """This does stuff!"""
        embed = discord.Embed(
            #color=await ctx.embed_colour(),
            color=discord.Color.from_rgb(255, 0, 255),
            description=""
        )

        embed.add_field(name="Submitter", value=f"Walnut (she/her/they/them)#8008", inline=False)

        fields = [
            "SUGGESTION",
            "IS YOUR IDEA AN EXISTING PLUGIN OR DATAPACK?",
            "WHY SHOULD WE ADD THIS SUGGESTION?",
            "ANY OTHER USEFUL INFORMATION"
            ]

        for i in range(len(fields)):
            currentContent = suggestion.split(f"**{fields[i]}**")

            await ctx.send(f"Found {len(currentContent)} of: **{fields[i]}**")

            if len(currentContent) > 2:
                return await ctx.send(f"Found two **{fields[i]}**")

        suggestion = suggestion.split(f"**SUGGESTION**: {suggestion}")

        await ctx.send(f"**SUGGESTION**: {suggestion}")

        embed.add_field(name="SUGGESTION", value=f"Special Heads for the months of May/June given out to recent graduates to celebrate our Dominionites RL Accomplishment", inline=False)
        embed.add_field(name="IS YOUR IDEA AN EXISTING PLUGIN OR DATAPACK?", value=f"no", inline=False)
        embed.add_field(name="WHY SHOULD WE ADD THIS SUGGESTION?", value=f"I think it would be a fun way to celebrate members of our community as that's a major life event for many people. We have a lot of younger people on the server and it would be a nice way to show some support.", inline=False)
        embed.add_field(name="ANY OTHER USEFUL INFORMATION", value=f"Just an addition for community spirit", inline=False)

        channel = get(ctx.guild.text_channels, id=800328370252415006)
        msg = await channel.send("", embed=embed)
        await msg.add_reaction("<:emoji:731293934822883429>")
        await msg.add_reaction("<:emoji:731293934856175687>")
