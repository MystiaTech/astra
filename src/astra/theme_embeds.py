"""
Theme-related Discord Embeds
============================
IMPLEMENTATION BY: Olivia (UX Lead)

Embeds for theme selection and management.
"""

import discord
from typing import Optional, List

from .themes import Theme, ThemeManager


COLORS = {
    "primary": 0x9B59B6,      # Mystic Purple
    "success": 0x2ECC71,      # Success Green
    "warning": 0xF39C12,      # Warning Orange
    "info": 0x3498DB,         # Info Blue
}


def create_theme_selection_embed(
    themes: List[Theme],
    user_name: str,
    is_first_time: bool = False
) -> discord.Embed:
    """
    Create the theme selection embed.
    
    Shown to users on first use or when changing themes.
    """
    if is_first_time:
        title = "🎨 Welcome to Astra! Choose Your Deck"
        description = (
            f"Hello {user_name}! Before we begin your tarot journey, "
            f"please select a card deck theme that resonates with you.\n\n"
            f"You can change this anytime with `/tarot-theme`."
        )
    else:
        title = "🎨 Select Your Card Theme"
        description = (
            f"Choose a tarot deck theme for your readings. "
            f"Each theme offers unique artwork and energy."
        )
    
    embed = discord.Embed(
        title=title,
        description=description,
        color=COLORS["primary"]
    )
    
    # Add each theme as a field
    for i, theme in enumerate(themes[:10], 1):  # Max 10 themes
        emoji = "⭐" if theme.is_default else "🃏"
        
        value_lines = [f"*{theme.description[:80]}...*" if len(theme.description) > 80 
                      else f"*{theme.description}*"]
        
        value_lines.append(f"\nBy: **{theme.author}**")
        value_lines.append(f"Cards: {'✓ Reversed support' if theme.supports_reversed else 'Standard'}")
        
        embed.add_field(
            name=f"{emoji} {i}. {theme.name}",
            value="\n".join(value_lines),
            inline=True
        )
    
    embed.set_footer(text="React with the number of your chosen theme 🌙")
    
    return embed


def create_theme_selected_embed(theme: Theme, user_name: str) -> discord.Embed:
    """Confirmation embed when a user selects a theme."""
    embed = discord.Embed(
        title="✅ Theme Selected",
        description=(
            f"**{user_name}**, you've chosen the **{theme.name}** deck!\n\n"
            f"*{theme.description}*\n\n"
            f"Your readings will now use this deck's imagery. "
            f"You can change themes anytime with `/tarot-theme`."
        ),
        color=COLORS["success"]
    )
    
    if theme.preview_image:
        embed.set_image(url=f"attachment://{theme.preview_image}")
    
    embed.set_footer(text="Ready to begin your reading? Use /tarot-single or another spread command! 🔮")
    
    return embed


def create_theme_list_embed(themes: List[Theme], manager: ThemeManager) -> discord.Embed:
    """Embed showing all available themes."""
    embed = discord.Embed(
        title="🎨 Available Tarot Themes",
        description=f"Astra has **{len(themes)}** card deck themes available.",
        color=COLORS["info"]
    )
    
    # Default theme first
    default_themes = [t for t in themes if t.is_default]
    other_themes = [t for t in themes if not t.is_default]
    
    for theme in default_themes + other_themes:
        status = "⭐ Default" if theme.is_default else "🃏"
        user_count = sum(1 for t in manager.user_preferences.values() if t == theme.id)
        
        value = f"*{theme.description[:60]}...*\n" if len(theme.description) > 60 else f"*{theme.description}*\n"
        value += f"By: {theme.author} • {user_count} users"
        
        embed.add_field(
            name=f"{status} {theme.name}",
            value=value,
            inline=False
        )
    
    embed.set_footer(text="Use /tarot-theme to switch decks 🌙")
    
    return embed


def create_theme_preview_embed(theme: Theme) -> discord.Embed:
    """Embed showing a preview of a specific theme."""
    embed = discord.Embed(
        title=f"🃏 {theme.name}",
        description=theme.description,
        color=COLORS["primary"]
    )
    
    embed.add_field(name="Author", value=theme.author, inline=True)
    embed.add_field(name="Version", value=theme.version, inline=True)
    embed.add_field(
        name="Reversed Cards", 
        value="✅ Yes" if theme.supports_reversed else "❌ No", 
        inline=True
    )
    
    if theme.metadata:
        extra_info = "\n".join(f"**{k}:** {v}" for k, v in list(theme.metadata.items())[:3])
        if extra_info:
            embed.add_field(name="Details", value=extra_info, inline=False)
    
    if theme.preview_image:
        embed.set_image(url=f"attachment://preview.png")
    
    return embed


def create_theme_help_embed() -> discord.Embed:
    """Help embed explaining the theme system."""
    embed = discord.Embed(
        title="🎨 About Tarot Themes",
        description=(
            "Astra supports multiple card deck themes, allowing you to "
            "choose artwork that resonates with your personal style and energy."
        ),
        color=COLORS["info"]
    )
    
    embed.add_field(
        name="Getting Started",
        value=(
            "On your first reading, you'll be asked to choose a theme. "
            "Select the one that calls to you!"
        ),
        inline=False
    )
    
    embed.add_field(
        name="Changing Themes",
        value="Use `/tarot-theme` anytime to switch to a different deck.",
        inline=False
    )
    
    embed.add_field(
        name="Adding New Themes",
        value=(
            "Server admins can add new themes by placing them in the "
            "`themes/` folder (top-level). New themes appear automatically!"
        ),
        inline=False
    )
    
    embed.add_field(
        name="Reversed Card Support",
        value=(
            "Some themes include unique artwork for reversed cards. "
            "Themes without reversed support will show upright cards rotated."
        ),
        inline=False
    )
    
    embed.set_footer(text="Each theme brings its own energy to your readings 🌟")
    
    return embed
