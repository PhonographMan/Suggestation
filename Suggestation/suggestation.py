import asyncio
import typing

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
        self.config = Config.get_conf(self, identifier=56546456456456553, force_registration=True)
        self.config.register_guild(
            listen_channel_id=None,
            sent_channel_id=None,
            suggestion_fields=["SUGGESTION"]
        )

    @commands.command()
    async def suggest(self, ctx: commands.Context, *, suggestion: str):
        roleMention = "<@&988180927903592538>"

        # Get a channel to send into
        sentChannel = ctx.channel
        configSentChannel = get(ctx.guild.text_channels, id=await self.config.guild(ctx.guild).sent_channel_id())
        if configSentChannel is not None:
            sentChannel = configSentChannel

        # Get the channel to listen from
        listenChannel = ctx.channel
        configListenChannel = get(ctx.guild.text_channels, id=await self.config.guild(ctx.guild).listen_channel_id())
        if configListenChannel is not None:
            listenChannel = configListenChannel

        if ctx.channel != listenChannel:
            return

        embed = discord.Embed(
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
                return await self.ErrorMessageBox(ctx,
                                                  f"Entered too many of this field: **{fields[i]}**")

            elif len(currentContent) == 1:
                return await self.ErrorMessageBox(ctx,
                                                  f"Field not found or nothing found within it, please enter something"
                                                  f"even if it is N/A for the field: **{fields[i]}**")

            elif len(currentContent) > 2:
                return await self.ErrorMessageBox(ctx,
                                                  f"Field not found or nothing found within it, please enter something"
                                                  f"even if it is N/A for the field: **{fields[i]}**")

            if i < len(fields) - 1:
                currentContent = currentContent[1].split(f"**{fields[i + 1]}**")

                if len(currentContent) == 1:
                    return await self.ErrorMessageBox(ctx,
                                                      f"Not enough fields in message. "
                                                      f"The field: {fields[i]} is not the last one.")

                currentContent = currentContent[0]

            else:
                currentContent = currentContent[1]

            embed.add_field(name=fields[i],
                            value=currentContent,
                            inline=False)

        embed.add_field(name="Suggestation by Lord_Bones",
                        value=roleMention,
                        inline=False)

        msg = await sentChannel.send("", embed=embed)
        await msg.add_reaction("<:emoji:731293934822883429>")
        await msg.add_reaction("<:emoji:731293934856175687>")
        await ctx.message.delete()

    async def ErrorMessageBox(
            self,
            ctx: commands.Context,
            suggestion: str
    ):
        embed = discord.Embed(
            title="Something went wrong",
            color=discord.Color.from_rgb(255, 0, 0),
            description=suggestion
        )

        msg = await ctx.send("", embed=embed)
        try:
            await self.bot.wait_for("reaction_add", timeout=30, check=msg)
        except asyncio.TimeoutError:
            await msg.delete()

    async def AcceptMessageBox(
            self,
            ctx: commands.Context,
            suggestion: str
    ):
        embed = discord.Embed(
            color=discord.Color.from_rgb(20, 219, 73),
            description=suggestion
        )

        msg = await ctx.send("", embed=embed)
        try:
            await self.bot.wait_for("reaction_add", timeout=30, check=msg)
        except asyncio.TimeoutError:
            await msg.delete()

    @commands.command(name="suggestation")
    async def CommandSuggestation(
            self,
            ctx: commands.Context,
            suggestion: str,
            first: typing.Union[discord.TextChannel, str] = "",
            second: typing.Union[int, str] = None,
            *,
            third: str = "",
    ):
        """
         CommandSuggestation Setup and modification command /suggestation

         :param ctx: The command which was sent
         :param suggestion: The sub-command name
         :param first: The input to the command. Many types.
         :return: Function awaits response
         """

        if suggestion == "listenchannel":
            if isinstance(first, discord.TextChannel):
                return await self.SetListenChannel(ctx, first)

            else:
                return await self.ErrorMessageBox(ctx, f"I didn't find that channel...")

        elif suggestion == "sentchannel":
            if isinstance(first, discord.TextChannel):
                return await self.SetSentChannel(ctx, first)

            else:
                return await self.ErrorMessageBox(ctx, f"I didn't find that channel...")

        elif suggestion == "list":
            return await self.ListSuggestFields(ctx)

        else:
            return await self.ErrorMessageBox(ctx, "Command not recognised.")

    async def SetListenChannel(
            self,
            ctx: commands.Context,
            channel: discord.TextChannel = None,
    ):
        """
        SetListenChannel Sets the channel suggestions is listening in by setting listen_channel_id config

        :param ctx: The command which was sent
        :param channel: Channel to update to. If blank will default to nothing.
        :return: Function awaits response
        """

        if not channel:
            await self.config.listen_channel_id.set(None)
            await ctx.message.delete()
            return await self.AcceptMessageBox(ctx, f"Suggestation will listen in all channels.")

        await self.config.guild(ctx.guild).listen_channel_id.set(channel.id)
        await ctx.message.delete()
        return await self.AcceptMessageBox(ctx, f"Suggestation will listen only to {channel.mention}")

    async def SetSentChannel(
            self,
            ctx: commands.Context,
            channel: discord.TextChannel = None,
    ):
        """
        SetSentChannel Sets the channel suggestions would be sent into by setting the config sent_channel.

        :param ctx: The command which was sent
        :param channel: Channel to update to. If blank will default to nothing.
        :return: Function awaits response
        """

        if not channel:
            await self.config.sent_channel_id.set(None)
            await ctx.message.delete()
            return await self.AcceptMessageBox(ctx, f"Suggestation send channel is reset to user channel")

        await self.config.guild(ctx.guild).sent_channel_id.set(channel.id)
        await ctx.message.delete()
        return await self.AcceptMessageBox(ctx, f"Suggestation will send to {channel.mention}")

    async def ListSuggestFields(
            self,
            ctx: commands.Context
    ):
        fieldsOutput = "No fields entered"
        async with self.config.guild(ctx.guild).suggestion_fields() as suggestionFields:

            if isinstance(suggestionFields, list):
                if len(suggestionFields) > 0:

                    # Merge Fields into a single string
                    fieldsOutput = ""
                    for i in range(len(suggestionFields)):
                        if fieldsOutput == "":
                            fieldsOutput = f"[{i}] - {suggestionFields[i]}"
                        else:
                            fieldsOutput = f"{fieldsOutput}\n[{i}] - {suggestionFields[i]}"

        embed = discord.Embed(
            title="Suggestion Fields",
            color=discord.Color.from_rgb(255, 0, 0),
            description=fieldsOutput
        )

        msg = await ctx.send("", embed=embed)