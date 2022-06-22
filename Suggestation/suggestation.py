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
        self.config = Config.get_conf(self, identifier=565464564564565533, force_registration=True)
        self.config.register_guild(
            listen_channel_id=None,
            sent_channel_id=None,
            suggestion_fields=["SUGGESTION"],
            mentioned_role=None,
            tick_emoji=None,
            cross_emoji=None,
        )

    @commands.command()
    async def suggest(self, ctx: commands.Context, *, suggestion: str):

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

        async with self.config.guild(ctx.guild).suggestion_fields() as fields:

            for i in range(len(fields)):
                field = fields[i].strip()

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

        roleMention = await self.config.guild(ctx.guild).mentioned_role()
        if roleMention is None:
            roleMention="·"

        embed.add_field(name="Suggestation by Lord_Bones",
            value=roleMention,
            inline=False)

        msg = await sentChannel.send("", embed=embed)

        tickEmoji = await self.config.guild(ctx.guild).tick_emoji()
        if tickEmoji is None:
            await msg.add_reaction("✅")

        else:
            await msg.add_reaction(tickEmoji)

        crossEmoji = await self.config.guild(ctx.guild).cross_emoji()
        if crossEmoji is None:
            await msg.add_reaction("❎")

        else:
            await msg.add_reaction(crossEmoji)

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
        except:
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
        except:  # asyncio.TimeoutError:
            await msg.delete()

    @commands.command(name="suggestation")
    async def CommandSuggestation(
            self,
            ctx: commands.Context,
            suggestion: str,
            first: typing.Union[discord.TextChannel, str, discord.Role, discord.Emoji] = "",
            *,
            second: str = "",
    ):
        """
         CommandSuggestation Setup and modification command /suggestation

         :param ctx: The command which was sent
         :param suggestion: The sub-command name
         :param first: The input to the command. Many types.
         :return: Function awaits response
         """

        suggestion.lower().strip()
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

        elif suggestion == "listfields":
            return await self.ListSuggestFields(ctx)

        elif suggestion == "addfield":
            field = f"{first} {second}"
            return await self.AddSuggestFieldToEnd(ctx, field)

        elif suggestion == "removefield":
            field = f"{first} {second}"

            return await self.RemoveSuggestField(ctx, field)

        elif suggestion == "insertfield":
            return await self.InsertSuggestField(ctx, first, second)

        elif suggestion == "resetfields":
            return await self.ResetFields(ctx)

        elif suggestion == "setrole":
            return await self.SetSuggestRole(ctx, first)

        elif suggestion == "settick":
            return await self.SetTickEmoji(ctx, first)

        elif suggestion == "setcross":
            return await self.SetCrossEmoji(ctx, first)

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
            await self.config.guild(ctx.guild).listen_channel_id.set(None)
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
            await self.config.guild(ctx.guild).sent_channel_id.set(None)
            await ctx.message.delete()
            return await self.AcceptMessageBox(ctx, f"Suggestation send channel is reset to user channel")

        await self.config.guild(ctx.guild).sent_channel_id.set(channel.id)
        await ctx.message.delete()
        return await self.AcceptMessageBox(ctx, f"Suggestation will send to {channel.mention}")

    async def ListSuggestFields(
            self,
            ctx: commands.Context
    ):
        """
        ListSuggestFields Lists fields for suggestions

        :param ctx: The command which was sent
        :return: Function awaits response
        """

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

        await ctx.message.delete()
        msg = await ctx.send("", embed=embed)

    async def AddSuggestFieldToEnd(
            self,
            ctx: commands.Context,
            newField: str,
    ):
        """
        AddSuggestFieldToEnd Add a field to the end

        :param ctx: The command which was sent
        :param newField: The new field to add
        :return: Function awaits response
        """

        if newField == "":
            return await self.ErrorMessageBox(ctx, f"Please enter something to remove from the field list")

        await ctx.message.delete()

        newField = newField.upper().strip()
        async with self.config.guild(ctx.guild).suggestion_fields() as suggestion_fields:
            if newField in suggestion_fields:
                return await self.ErrorMessageBox(ctx, f"Suggestation field {newField} already in the list.")

            suggestion_fields.append(f"{newField}")
        return await self.AcceptMessageBox(ctx, f"Suggestation field added to end: {newField}")

    async def RemoveSuggestField(
            self,
            ctx: commands.Context,
            removeField: str
    ):
        """
        RemoveSuggestField Removes the given field

        :param ctx: The command which was sent
        :param removeField: Field to remove
        :return: Function awaits response
        """

        removeField = removeField.strip()

        if removeField.lower() == "help":
            await ctx.message.delete()
            return await ctx.send("```md\n"
                "# !suggestation removeField <TEXT>\n"
                "[⛰️]<RemoveField Removes the given field>\n"
                "[📝]<Text The field to remove. Fields are not case sensitive.>\n"
                "```")

        if removeField == "":
            return await self.ErrorMessageBox(ctx, f"Please enter something to remove from the field list")

        removeField = removeField.upper().strip()
        async with self.config.guild(ctx.guild).suggestion_fields() as suggestion_fields:
            if removeField not in suggestion_fields:
                return await self.ErrorMessageBox(ctx, f"Suggestation field {removeField} already isn't the list.")

            suggestion_fields.remove(f"{removeField}")
            if len(suggestion_fields) == 0:
                suggestion_fields.append("SUGGESTION")

        await ctx.message.delete()
        return await self.AcceptMessageBox(ctx, f"Suggestation field removed {removeField}")

    async def InsertSuggestField(
            self,
            ctx: commands.Context,
            index: str = "",
            newField: str = "",
    ):
        """
        InsertSuggestField Inserts a field after an index

        :param ctx: The command which was sent
        :param index: Index to insert at
        :param newField: New field to insert
        :return: Function awaits response
        """
        index = index.strip()

        if index.lower() == "help":
            await ctx.message.delete()
            return await ctx.send("```md\n"
                "# !suggestation insertfield <NUMBER> <TEXT>\n"
                "[⛰️]<InsertField Inserts a new field at a given location>\n"
                "[🔟]<Number The number to insert the field before. Use listfields to get an idea of these.>\n"
                "[📝]<Text The new field to insert at that location>\n"
                "```")

        if index == "":
            return await self.ErrorMessageBox(ctx, f"Please enter the index to insert at."
                                                   f"To see the index use listfields")

        elif newField == "":
            return await self.ErrorMessageBox(ctx, f"Please insert the new field.")

        try:
            indexAsInt = int(index)

        except ValueError:
            return await self.ErrorMessageBox(ctx, f"Index is not a number")

        newField = newField.upper().strip()
        async with self.config.guild(ctx.guild).suggestion_fields() as suggestion_fields:
            if newField in suggestion_fields:
                return await self.ErrorMessageBox(ctx, f"Suggestation field {newField} already in the list.")

            if indexAsInt < 0:
                indexAsInt = 0
            elif indexAsInt > len(suggestion_fields) - 1:
                indexAsInt = len(suggestion_fields) - 1

            suggestion_fields.insert(indexAsInt, newField)

        await ctx.message.delete()
        return await self.AcceptMessageBox(ctx, f"Suggestation field added to end: {newField}")

    async def ResetFields(
            self,
            ctx: commands.Context,
    ):
        """
        ResetFields Resets fields to default

        :param ctx: The command which was sent
        :return: Function awaits response
        """

        embed = discord.Embed(
            title="Are you sure?",
            color=discord.Color.from_rgb(255, 0, 0),
            description="Are you sure you would like to reset the fields?"
        )
        msg = await ctx.send("", embed=embed)
        start_adding_reactions(msg, ReactionPredicate.YES_OR_NO_EMOJIS)
        pred = ReactionPredicate.yes_or_no(msg, ctx.author)

        try:
            await self.bot.wait_for("reaction_add", timeout=30, check=pred)

        except asyncio.TimeoutError:
            await msg.delete()
            return await self.ErrorMessageBox(ctx, "You took too long. Try again, please.")

        # This means they chose no
        if not pred.result:
            return await msg.delete()

        async with self.config.guild(ctx.guild).suggestion_fields() as suggestion_fields:
            suggestion_fields.clear()
            suggestion_fields.append("SUGGESTION")

            await ctx.message.delete()
            return await self.AcceptMessageBox(ctx, f"Suggestation fields have been reset")

    async def SetSuggestRole(
            self,
            ctx: commands.Context,
            role: discord.Role = None,
    ):
        """
        SetSuggestRole Sets the role to mention in the suggestions

        :param ctx: The command which was sent
        :param role: The role to update
        :return: Function awaits response
        """

        if not role:
            await self.config.guild(ctx.guild).mentioned_role.set(None)
            await ctx.message.delete()
            return await self.AcceptMessageBox(ctx, f"Suggestation mention role is reset to nothing.")

        await self.config.guild(ctx.guild).mentioned_role.set(role)
        await ctx.message.delete()
        return await self.AcceptMessageBox(ctx, f"Suggestation will send {role} role")

    async def SetTickEmoji(
            self,
            ctx: commands.Context,
            emoji: discord.Emoji = None,
    ):
        """
        SetTickEmoji Sets the first emoji on the suggestion

        :param ctx: The command which was sent
        :param emoji: The emoji to attach
        :return: Function awaits response
        """

        if not emoji:
            await self.config.guild(ctx.guild).tick_emoji.set(None)
            await ctx.message.delete()
            return await self.AcceptMessageBox(ctx, f"Suggestation first emoji is reset to nothing.")

        await self.config.guild(ctx.guild).tick_emoji.set(emoji)
        await ctx.message.delete()
        return await self.AcceptMessageBox(ctx, f"Suggestation will attach {emoji} first on suggestions")

    async def SetCrossEmoji(
            self,
            ctx: commands.Context,
            emoji: discord.Emoji = None,
    ):
        """
        SetCrossEmoji Sets the second emoji on the suggestion

        :param ctx: The command which was sent
        :param emoji: The emoji to attach
        :return: Function awaits response
        """

        if not emoji:
            await self.config.guild(ctx.guild).cross_emoji.set(None)
            await ctx.message.delete()
            return await self.AcceptMessageBox(ctx, f"Suggestation second emoji is reset to nothing.")

        await self.config.guild(ctx.guild).cross_emoji.set(emoji)
        await ctx.message.delete()
        return await self.AcceptMessageBox(ctx, f"Suggestation will attach {emoji} second on suggestions")
