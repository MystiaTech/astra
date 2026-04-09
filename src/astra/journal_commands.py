"""
Journal Slash Commands
======================
IMPLEMENTATION BY: Emma (Backend Lead)
UI BY: Olivia (UX Lead)

Commands for the personal reading journal system.
"""

from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from .embeds import create_journal_embed, create_journal_entry_embed
from .journal import get_journal_manager
from .reading import Reading


class JournalCommands(commands.Cog):
    """Journal management slash commands."""

    def __init__(self, bot):
        self.bot = bot
        self.journal_manager = get_journal_manager()

    @app_commands.command(name="tarot-journal", description="View your saved readings")
    @app_commands.describe(page="Page number to view")
    async def tarot_journal(self, interaction: discord.Interaction, page: Optional[int] = 1):
        """View user's reading journal."""
        await interaction.response.defer(thinking=True, ephemeral=True)

        readings = self.journal_manager.get_user_readings(interaction.user.id)

        embed = create_journal_embed(readings, interaction.user, page=page)

        # Add navigation buttons if needed
        total_pages = (len(readings) + 4) // 5 if readings else 1

        if total_pages > 1:
            view = discord.ui.View()

            if page > 1:
                prev_btn = discord.ui.Button(
                    label="◀ Previous", style=discord.ButtonStyle.secondary
                )

                async def prev_callback(inter):
                    await self.tarot_journal.callback(self, inter, page=page - 1)

                prev_btn.callback = prev_callback
                view.add_item(prev_btn)

            if page < total_pages:
                next_btn = discord.ui.Button(label="Next ▶", style=discord.ButtonStyle.secondary)

                async def next_callback(inter):
                    await self.tarot_journal.callback(self, inter, page=page + 1)

                next_btn.callback = next_callback
                view.add_item(next_btn)

            await interaction.followup.send(embed=embed, view=view, ephemeral=True)
        else:
            await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="tarot-save", description="Save the last reading to your journal")
    async def tarot_save(self, interaction: discord.Interaction):
        """Save the most recent reading to journal."""
        await interaction.response.defer(thinking=True, ephemeral=True)

        # Get the last reading from the bot's memory
        # For now, we'll need to store it temporarily
        # This is a simplified version - in production, store reading in user session

        await interaction.followup.send(
            "💫 To save a reading, use the Save button that appears with your reading result!",
            ephemeral=True,
        )

    @app_commands.command(name="tarot-journal-view", description="View a specific journal entry")
    @app_commands.describe(entry_id="The entry number from your journal")
    async def tarot_journal_view(self, interaction: discord.Interaction, entry_id: int):
        """View a specific journal entry in detail."""
        await interaction.response.defer(thinking=True, ephemeral=True)

        entry = self.journal_manager.get_entry(interaction.user.id, entry_id)

        if not entry:
            await interaction.followup.send(
                "❌ Entry not found. Use `/tarot-journal` to see your saved readings.",
                ephemeral=True,
            )
            return

        embed = create_journal_entry_embed(entry.to_dict(), interaction.user)
        await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="tarot-journal-delete", description="Delete a journal entry")
    @app_commands.describe(entry_id="The entry number to delete")
    async def tarot_journal_delete(self, interaction: discord.Interaction, entry_id: int):
        """Delete a specific journal entry."""
        await interaction.response.defer(thinking=True, ephemeral=True)

        success = self.journal_manager.delete_entry(interaction.user.id, entry_id)

        if success:
            await interaction.followup.send(
                f"🗑️ Entry #{entry_id} has been deleted from your journal.", ephemeral=True
            )
        else:
            await interaction.followup.send(
                "❌ Could not delete entry. It may not exist.", ephemeral=True
            )

    @app_commands.command(name="tarot-journal-stats", description="View your reading statistics")
    async def tarot_journal_stats(self, interaction: discord.Interaction):
        """View statistics about user's readings."""
        await interaction.response.defer(thinking=True, ephemeral=True)

        stats = self.journal_manager.get_stats(interaction.user.id)

        if stats["total_readings"] == 0:
            await interaction.followup.send(
                "📊 You haven't saved any readings yet. Start with `/tarot-single`!", ephemeral=True
            )
            return

        embed = discord.Embed(
            title="📊 Your Reading Statistics",
            description=f"Insights from your tarot journey, {interaction.user.display_name}",
            color=0x9B59B6,
        )

        embed.add_field(name="Total Readings", value=str(stats["total_readings"]), inline=True)
        embed.add_field(
            name="Favorite Spread",
            value=stats["most_common_spread"] or "N/A",
            inline=True,
        )

        if stats["first_reading"]:
            embed.add_field(name="First Reading", value=stats["first_reading"][:10], inline=True)

        if stats["latest_reading"]:
            embed.add_field(name="Latest Reading", value=stats["latest_reading"][:10], inline=True)

        await interaction.followup.send(embed=embed, ephemeral=True)


async def save_reading_to_journal(
    user_id: str, reading: Reading, interaction: discord.Interaction
) -> bool:
    """
    Save a reading to the user's journal.
    Called after a reading is completed.
    """
    manager = get_journal_manager()

    # Convert cards to serializable format
    cards_data = []
    for result in reading.results:
        cards_data.append(
            {
                "name": result.card.get_display_name(result.reversed),
                "position": result.position,
                "reversed": result.reversed,
                "meaning": result.get_interpretation()[:500],  # Truncate for storage
                "keywords": result.get_keywords(),
            }
        )

    entry = manager.save_reading(
        user_id=user_id,
        spread_type=reading.spread_type,
        question=reading.question,
        cards=cards_data,
        interpretation=None,  # Could add AI interpretation later
        notes=None,
    )

    return entry is not None
