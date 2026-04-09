"""
Discord Embeds for Astra
========================
IMPLEMENTATION BY: Olivia (UX/Frontend Lead)

Rich embeds for displaying tarot readings with beautiful formatting.
"""

import discord
from typing import Optional

from .data import Card, Spread, SpreadPosition
from .reading import Reading, ReadingResult


# Color palette for embeds
COLORS = {
    "primary": 0x9B59B6,      # Mystic Purple
    "secondary": 0xE74C3C,    # Reversed Red
    "major_arcana": 0xF1C40F, # Gold
    "wands": 0xE67E22,        # Fire Orange
    "cups": 0x3498DB,         # Water Blue
    "swords": 0x95A5A6,       # Air Silver
    "pentacles": 0x27AE60,    # Earth Green
    "info": 0x3498DB,         # Info Blue
    "success": 0x2ECC71,      # Success Green
    "warning": 0xF39C12,      # Warning Orange
}

SUIT_EMOJIS = {
    "MAJOR": "🌟",
    "WANDS": "🔥",
    "CUPS": "💧",
    "SWORDS": "💨",
    "PENTACLES": "🌍",
}

POSITION_EMOJIS = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]


def get_card_color(card: Card, reversed: bool = False) -> int:
    """Get the appropriate color for a card."""
    if reversed:
        return COLORS["secondary"]
    
    suit_colors = {
        "MAJOR": COLORS["major_arcana"],
        "WANDS": COLORS["wands"],
        "CUPS": COLORS["cups"],
        "SWORDS": COLORS["swords"],
        "PENTACLES": COLORS["pentacles"],
    }
    return suit_colors.get(card.suit.name, COLORS["primary"])


def get_suit_emoji(card: Card) -> str:
    """Get the emoji for a card's suit."""
    return SUIT_EMOJIS.get(card.suit.name, "🃏")


def create_reading_embed(
    reading: Reading,
    user: discord.User,
    spread: Spread
) -> discord.Embed:
    """
    Create the main reading result embed.
    
    This is the primary display for a completed tarot reading.
    """
    # Main embed
    embed = discord.Embed(
        title=f"🔮 {spread.name}",
        description=_create_reading_description(reading, spread),
        color=COLORS["primary"],
        timestamp=reading.timestamp
    )
    
    # Add question if provided
    if reading.question:
        embed.add_field(
            name="❓ Question",
            value=f"*{reading.question}*",
            inline=False
        )
    
    # Add each card as a field
    for i, result in enumerate(reading.results):
        position = spread.positions[i] if i < len(spread.positions) else None
        field_value = _create_card_field_value(result, position)
        
        embed.add_field(
            name=_create_card_field_name(result, position),
            value=field_value,
            inline=False
        )
    
    # Add summary/interpretation
    summary = _create_reading_summary(reading, spread)
    if summary:
        embed.add_field(
            name="🌙 Reading Summary",
            value=summary,
            inline=False
        )
    
    # Footer
    embed.set_footer(
        text=f"Reading for {user.display_name} • {len(reading.results)} cards • "
             f"{reading.count_reversed()} reversed",
        icon_url=user.display_avatar.url if user.display_avatar else None
    )
    
    # Thumbnail - placeholder for now
    embed.set_thumbnail(url="attachment://astra_icon.png")
    
    return embed


def _create_reading_description(reading: Reading, spread: Spread) -> str:
    """Create the embed description."""
    lines = [
        f"*{spread.description}*",
        "",
        f"This reading uses **{spread.num_cards} cards** and takes approximately "
        f"**{spread.estimated_time}** to contemplate.",
    ]
    return "\n".join(lines)


def _create_card_field_name(result: ReadingResult, position: Optional[SpreadPosition]) -> str:
    """Create the field name for a card."""
    emoji = POSITION_EMOJIS[result.position - 1] if result.position <= len(POSITION_EMOJIS) else "🃏"
    suit_emoji = get_suit_emoji(result.card)
    card_name = result.card.get_display_name(reversed=result.reversed)
    
    if position:
        return f"{emoji} Position {result.position}: {position.name}\n{suit_emoji} {card_name}"
    else:
        return f"{emoji} {card_name}"


def _create_card_field_value(result: ReadingResult, position: Optional[SpreadPosition]) -> str:
    """Create the field value for a card."""
    lines = []
    
    # Position meaning
    if position:
        lines.append(f"**{position.meaning}**")
        lines.append(f"*{position.description[:100]}...*" if len(position.description) > 100 
                     else f"*{position.description}*")
        lines.append("")
    
    # Keywords
    keywords = result.get_keywords()
    keyword_str = " • ".join(f"`{k}`" for k in keywords[:4])
    lines.append(f"**Keywords:** {keyword_str}")
    
    # Interpretation
    interpretation = result.get_interpretation()
    # Truncate if too long
    if len(interpretation) > 200:
        interpretation = interpretation[:197] + "..."
    lines.append(f"\n{interpretation}")
    
    return "\n".join(lines)


def _create_reading_summary(reading: Reading, spread: Spread) -> str:
    """Create a summary interpretation of the reading."""
    lines = []
    
    # Count suits
    suit_counts = {}
    major_count = 0
    for result in reading.results:
        if result.card.is_major:
            major_count += 1
        else:
            suit = result.card.suit.name
            suit_counts[suit] = suit_counts.get(suit, 0) + 1
    
    # Elemental balance interpretation
    if major_count >= len(reading.results) / 2:
        lines.append("🌟 **Major Arcana Dominant**: Significant life lessons and karmic forces are at work. "
                    "This situation carries deep spiritual significance.")
    elif suit_counts:
        dominant_suit = max(suit_counts, key=suit_counts.get)
        suit_meanings = {
            "WANDS": "🔥 **Fire Energy (Wands)**: Action, creativity, and passion drive this situation. "
                    "Focus on initiative and personal power.",
            "CUPS": "💧 **Water Energy (Cups)**: Emotions, relationships, and intuition are central. "
                   "Trust your feelings and connections.",
            "SWORDS": "💨 **Air Energy (Swords)**: Intellect, communication, and decisions matter most. "
                     "Clear thinking will guide you.",
            "PENTACLES": "🌍 **Earth Energy (Pentacles)**: Material concerns, stability, and practical matters "
                        "are the focus. Ground yourself in reality.",
        }
        if dominant_suit in suit_meanings:
            lines.append(suit_meanings[dominant_suit])
    
    # Reversed cards note
    reversed_count = reading.count_reversed()
    if reversed_count > len(reading.results) / 2:
        lines.append("\n🔄 **Many Reversed Cards**: Internal or blocked energies are significant. "
                    "Consider what may need to be released or reconsidered.")
    elif reversed_count == 0 and len(reading.results) >= 3:
        lines.append("\n✨ **All Cards Upright**: Clear, direct energy flows through this situation. "
                    "The path forward is relatively unobstructed.")
    
    return "\n".join(lines) if lines else ""


def create_spread_info_embed() -> discord.Embed:
    """Create an embed showing all available spreads."""
    from .data import SPREADS, SPREAD_DISPLAY_ORDER
    
    embed = discord.Embed(
        title="🔮 Available Tarot Spreads",
        description="Astra offers several spreads for different types of inquiries. "
                   "Choose the one that best fits your needs.",
        color=COLORS["info"]
    )
    
    for spread_key in SPREAD_DISPLAY_ORDER:
        spread = SPREADS[spread_key]
        
        # Create field value
        value_lines = [
            f"*{spread.description}*",
            f"\n**Cards:** {spread.num_cards}",
            f"**Time:** ~{spread.estimated_time}",
            f"**Difficulty:** {spread.difficulty}",
            "\n**Best for:**"
        ]
        
        # Add best uses
        for use in spread.best_for[:3]:
            value_lines.append(f"• {use}")
        
        # Command reference
        cmd_name = spread_key.replace("_", "-")
        value_lines.append(f"\n*Use: `/tarot-{cmd_name}`*")
        
        embed.add_field(
            name=f"📜 {spread.name}",
            value="\n".join(value_lines),
            inline=True
        )
    
    embed.set_footer(
        text="Astra serves one seeker at a time to provide focused readings 🌙"
    )
    
    return embed


def create_help_embed() -> discord.Embed:
    """Create the help embed."""
    embed = discord.Embed(
        title="🔮 Astra - Tarot Reading Bot",
        description=(
            "Welcome, seeker. I am Astra, your guide through the mysteries of the tarot. "
            "I offer authentic readings using the wisdom of the 78 cards.\n\n"
            "**I serve one seeker at a time** to ensure each reading receives "
            "my full attention and energy."
        ),
        color=COLORS["primary"]
    )
    
    # Commands section
    embed.add_field(
        name="📖 Reading Commands",
        value=(
            "`/tarot-single` - Quick single card guidance\n"
            "`/tarot-three` - Past, Present, Future spread\n"
            "`/tarot-mind-body-spirit` - Holistic self-examination\n"
            "`/tarot-situation-action` - Problem-solving spread\n"
            "`/tarot-relationship` - Relationship dynamics\n"
            "`/tarot-career` - Career guidance\n"
            "`/tarot-celtic` - Full Celtic Cross (10 cards)"
        ),
        inline=False
    )
    
    embed.add_field(
        name="ℹ️ Information Commands",
        value=(
            "`/tarot-spreads` - Learn about all spreads\n"
            "`/tarot-help` - Show this help message\n"
            "`/tarot-cancel` - Cancel your current reading"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🃏 About Reversed Cards",
        value=(
            "Each reading allows reversed cards by default. Reversed cards "
            "offer additional depth, showing blocked energy, internal dynamics, "
            "or alternative perspectives. You can disable them in any command."
        ),
        inline=False
    )
    
    embed.add_field(
        name="✨ Tips for Best Results",
        value=(
            "• Take time to contemplate each card\n"
            "• Consider how cards relate to each other\n"
            "• Trust your intuition about the meanings\n"
            "• The future is not fixed—use readings as guidance\n"
            "• Return when you feel called to"
        ),
        inline=False
    )
    
    embed.set_footer(text="May the stars guide your path 🌟")
    
    return embed


def create_waiting_embed(position: int, total_users: int) -> discord.Embed:
    """Create an embed for when users are waiting."""
    embed = discord.Embed(
        title="🔮 Please Wait",
        description=(
            f"You are **position {position}** in line.\n\n"
            f"Astra serves one seeker at a time to ensure each reading "
            f"receives her full attention. There {'is' if total_users == 1 else 'are'} "
            f"{total_users} user{'s' if total_users != 1 else ''} ahead of you."
        ),
        color=COLORS["warning"]
    )
    return embed


def create_session_expired_embed() -> discord.Embed:
    """Create an embed for expired sessions."""
    return discord.Embed(
        title="🔮 Session Expired",
        description=(
            "Your reading session has expired after 5 minutes of inactivity.\n\n"
            "If you would like another reading, please use a tarot command again."
        ),
        color=COLORS["secondary"]
    )


def create_card_detail_embed(result: ReadingResult) -> discord.Embed:
    """
    Create a detailed embed for a single card.
    
    Useful for deep card study or daily card draws.
    """
    card = result.card
    color = get_card_color(card, result.reversed)
    
    embed = discord.Embed(
        title=f"{get_suit_emoji(card)} {card.get_display_name(result.reversed)}",
        description=result.get_interpretation(),
        color=color
    )
    
    # Keywords
    keywords = result.get_keywords()
    embed.add_field(
        name="Keywords",
        value=" • ".join(f"`{k}`" for k in keywords),
        inline=False
    )
    
    # Card details
    if card.is_major:
        embed.add_field(name="Arcana", value="Major Arcana", inline=True)
    else:
        embed.add_field(name="Suit", value=card.suit.name.title(), inline=True)
        if card.element:
            embed.add_field(name="Element", value=card.element, inline=True)
    
    if card.astrology:
        embed.add_field(name="Astrology", value=card.astrology, inline=True)
    
    # Image placeholder note
    embed.set_image(url=f"attachment://{card.image_placeholder}")
    
    return embed
