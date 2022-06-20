import discord
from discord import client
from discord.utils import get
from redbot.core import commands, Config
from redbot.core.utils import embed
from redbot.core.utils.menus import start_adding_reactions
from redbot.core.utils.predicates import ReactionPredicate

class Suggestation(commands.Cog):
    """My custom cog"""

    def __init__(self, bot):
        self.bot = bot
        self.config = Config.get_conf(self, identifier=2115656421364, force_registration=True)
        self.config.register_global(server_id=None, listen_channel_id=None, sent_channel_id=None)

    @commands.command()
    async def suggest(self, ctx: commands.Context, *, suggestion: str):
        # 800328370252415006
        #suggestionChannel = 732054706381127740
        #suggestionPostChannel = 732054706381127740
        roleMention = "<@&988180927903592538>"

        sentChannel = ctx.channel
        if self.config.sent_channel_id is not None:
            sentChannel = self.config.sent_channel_id

        listenChannel = ctx.channel
        if self.config.listen_channel_id is not None:
            listenChannel = self.config.listen_channel_id


        if ctx.channel.id != listenChannel:
            return

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

            if len(currentContent) > 2:
                return await ctx.send(f"Entered too many of this field: **{fields[i]}**")

            elif len(currentContent) == 1:
                return await ctx.send(f"Field not found or nothing found within it, please enter something"
                                      f"even if it is N/A for the field: **{fields[i]}**")

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

        embed.add_field(name="Suggestation by Lord_Bones",
                        value=roleMention,
                        inline=False)

        channel = get(ctx.guild.text_channels, id=sentChannel)
        msg = await channel.send("", embed=embed)
        await msg.add_reaction("<:emoji:731293934822883429>")
        await msg.add_reaction("<:emoji:731293934856175687>")
        await ctx.message.delete()

    @commands.command(name="suggestation listenchannel")
    async def setsuggest_setglobal_listenchannel(
        self,
        ctx: commands.Context,
        #server: discord.Guild = None,
        channel: discord.TextChannel = None,
    ):
        """Add channel where global suggestions should be sent."""
        #if not server:
        #    server = ctx.guild
        if not channel:
            channel = ctx.channel
        #await self.config.server_id.set(server.id)
        await self.config.listen_channel_id.set(channel.id)
        await ctx.send(f"Suggestation will listen in {channel.mention}")

    @commands.command(name="suggestation sentchannel")
    async def setsuggest_setglobal_sentchannel(
        self,
        ctx: commands.Context,
        server: discord.Guild = None,
        channel: discord.TextChannel = None,
    ):
        """Add channel where global suggestions should be sent."""
        #if not server:
        #    server = ctx.guild
        if not channel:
            channel = ctx.channel
        #await self.config.server_id.set(server.id)
        await self.config.sent_channel_id.set(channel.id)
        await ctx.send(f"Suggestation will sent to {channel.mention}")
