"""
Theme-related Slash Commands
============================
IMPLEMENTATION BY: Emma (Backend Lead)
UI BY: Olivia (UX Lead)

Commands for theme selection and management.
"""

import asyncio
import discord
from discord import app_commands
from discord.ext import commands

from .themes import get_theme_manager, Theme
from .theme_embeds import (
    create_theme_selection_embed,
    create_theme_selected_embed,
    create_theme_list_embed,
    create_theme_preview_embed,
    create_theme_help_embed,
)


class ThemeCommands(commands.Cog):
    """
    Theme management slash commands.
    
    Allows users to select and preview card themes.
    """
    
    def __init__(self, bot):
        self.bot = bot
        self.theme_manager = get_theme_manager(bot)
    
    @app_commands.command(name="tarot-themes", description="Browse available card themes")
    async def tarot_themes(self, interaction: discord.Interaction):
        """List all available themes."""
        themes = self.theme_manager.get_available_themes()
        
        if not themes:
            await interaction.response.send_message(
                "No themes available. Please contact the server administrator.",
                ephemeral=True
            )
            return
        
        embed = create_theme_list_embed(themes, self.theme_manager)
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="tarot-theme", description="Select your card theme")
    async def tarot_theme(self, interaction: discord.Interaction):
        """Show theme selection UI."""
        themes = self.theme_manager.get_available_themes()
        
        if len(themes) == 0:
            await interaction.response.send_message(
                "No themes available.",
                ephemeral=True
            )
            return
        
        if len(themes) == 1:
            await interaction.response.send_message(
                f"Only one theme is available: **{themes[0].name}**",
                ephemeral=True
            )
            return
        
        # Check if first time
        is_first_time = not self.theme_manager.has_selected_theme(interaction.user.id)
        
        embed = create_theme_selection_embed(
            themes=themes,
            user_name=interaction.user.display_name,
            is_first_time=is_first_time
        )
        
        # Create select menu
        options = []
        for i, theme in enumerate(themes[:25], 1):  # Max 25 options
            emoji = "⭐" if theme.is_default else "🃏"
            options.append(
                discord.SelectOption(
                    label=f"{i}. {theme.name}",
                    value=theme.id,
                    description=theme.description[:100],
                    emoji=emoji
                )
            )
        
        select = discord.ui.Select(
            placeholder="Choose your deck theme...",
            options=options,
            custom_id="theme_select"
        )
        
        async def select_callback(interaction: discord.Interaction):
            theme_id = select.values[0]
            theme = self.theme_manager.get_theme(theme_id)
            
            if theme:
                self.theme_manager.set_user_theme(interaction.user.id, theme_id)
                
                confirm_embed = create_theme_selected_embed(
                    theme=theme,
                    user_name=interaction.user.display_name
                )
                
                await interaction.response.send_message(embed=confirm_embed)
        
        select.callback = select_callback
        
        view = discord.ui.View()
        view.add_item(select)
        
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    @app_commands.command(name="tarot-theme-preview", description="Preview a specific theme")
    @app_commands.describe(theme_name="Name of the theme to preview")
    async def tarot_theme_preview(
        self,
        interaction: discord.Interaction,
        theme_name: str
    ):
        """Preview a specific theme."""
        # Find theme by name (case-insensitive)
        theme = None
        for t in self.theme_manager.get_available_themes():
            if t.name.lower() == theme_name.lower() or t.id.lower() == theme_name.lower():
                theme = t
                break
        
        if not theme:
            available = ", ".join(t.name for t in self.theme_manager.get_available_themes())
            await interaction.response.send_message(
                f"Theme '{theme_name}' not found. Available: {available}",
                ephemeral=True
            )
            return
        
        embed = create_theme_preview_embed(theme)
        
        files = []
        if theme.preview_image:
            preview_path = f"{theme.path}/{theme.preview_image}"
            try:
                files.append(discord.File(preview_path, filename="preview.png"))
            except:
                pass
        
        if files:
            await interaction.response.send_message(embed=embed, files=files)
        else:
            await interaction.response.send_message(embed=embed)
    
    @app_commands.command(name="tarot-theme-help", description="Learn about themes")
    async def tarot_theme_help(self, interaction: discord.Interaction):
        """Show theme help."""
        embed = create_theme_help_embed()
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    @app_commands.command(name="tarot-my-theme", description="Check your current theme")
    async def tarot_my_theme(self, interaction: discord.Interaction):
        """Show user's current theme."""
        theme = self.theme_manager.get_user_theme(interaction.user.id)
        
        if not theme:
            await interaction.response.send_message(
                "You haven't selected a theme yet. Use `/tarot-theme` to choose one!",
                ephemeral=True
            )
            return
        
        embed = discord.Embed(
            title="🎨 Your Current Theme",
            description=f"You are using the **{theme.name}** deck.",
            color=0x9B59B6
        )
        
        embed.add_field(name="Description", value=theme.description, inline=False)
        embed.add_field(name="Author", value=theme.author, inline=True)
        embed.add_field(name="Version", value=theme.version, inline=True)
        
        if theme.supports_reversed:
            embed.add_field(
                name="Reversed Cards",
                value="✅ This theme has unique reversed artwork",
                inline=False
            )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)


async def check_user_theme(bot, user_id: str) -> bool:
    """
    Check if a user has selected a theme.
    
    Returns True if they have, False if we need to prompt them.
    """
    manager = get_theme_manager(bot)
    return manager.has_selected_theme(user_id)


async def prompt_theme_selection(bot, interaction: discord.Interaction) -> bool:
    """
    Prompt user to select a theme if they haven't already.
    
    Returns True if user selected a theme, False if cancelled.
    """
    manager = get_theme_manager(bot)
    
    if manager.has_selected_theme(interaction.user.id):
        return True
    
    # Show theme selection
    themes = manager.get_available_themes()
    
    if len(themes) <= 1:
        # Auto-select default if only one theme
        if themes:
            manager.set_user_theme(interaction.user.id, themes[0].id)
        return True
    
    embed = create_theme_selection_embed(
        themes=themes,
        user_name=interaction.user.display_name,
        is_first_time=True
    )
    
    options = []
    for theme in themes[:25]:
        emoji = "⭐" if theme.is_default else "🃏"
        options.append(
            discord.SelectOption(
                label=theme.name,
                value=theme.id,
                description=theme.description[:100],
                emoji=emoji
            )
        )
    
    select = discord.ui.Select(
        placeholder="Choose your deck theme...",
        options=options
    )
    
    selected = False
    
    async def callback(inter):
        nonlocal selected
        theme_id = select.values[0]
        theme = manager.get_theme(theme_id)
        
        if theme:
            manager.set_user_theme(interaction.user.id, theme_id)
            confirm = create_theme_selected_embed(theme, interaction.user.display_name)
            await inter.response.send_message(embed=confirm, ephemeral=True)
            selected = True
    
    select.callback = callback
    
    view = discord.ui.View(timeout=120)
    view.add_item(select)
    
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
    
    # Wait for selection
    await asyncio.wait_for(view.wait(), timeout=120)
    
    return selected
