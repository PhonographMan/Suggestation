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
    async def suggest(self, ctx: commands.Context, *, suggestion: str):
        """This does stuff!"""
        embed = discord.Embed(
            # color=await ctx.embed_colour(),
            color=discord.Color.from_rgb(255, 0, 255)
        )

        embed.set_thumbnail(url=f"{ctx.author.avatar_url}")

        player = f"{ctx.author.name}#{ctx.author.discriminator}"
        embed.add_field(name="SUBMITTER", value=player, inline=False)

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
                #return await ctx.send(f"Entered too many of this field: **{fields[i]}**")
                return self.ErrorReturn(sender=ctx, message=f"Entered too many of this field: **{fields[i]}**")

            elif len(currentContent) > 2:
                return await ctx.send(f"Field not found or nothing found within it, please enter something"
                                      f"even if it is N/A for the field: **{fields[i]}**")

            if i < len(fields) - 1:
                currentContent = currentContent[1].split(f"**{fields[i + 1]}**")

                if len(currentContent) == 1:
                    return await ctx.send(f"Not enough fields in message. The field: {fields[i]} is not the last one.")

                currentContent = currentContent[0]

            else:
                currentContent = currentContent[1]

            embed.add_field(name=fields[i],
                            value=currentContent,
                            inline=False)

        channel = get(ctx.guild.text_channels, id=732054706381127740)  # 800328370252415006
        msg = await channel.send("", embed=embed)
        await msg.add_reaction("<:emoji:731293934822883429>")
        await msg.add_reaction("<:emoji:731293934856175687>")
        await ctx.message.delete()

    async def ErrorReturn(self, sender, message):
        embed = discord.Embed(color=discord.Color.from_rgb(255, 0, 000))

        embed.add_field(name="ERROR ADDING SUGGESTION", value=message, inline=False)
        await sender.send("", embed=embed)
