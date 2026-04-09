"""
Discord Embeds for Astra
========================
IMPLEMENTATION BY: Olivia (UX Lead)

Rich embeds for displaying tarot readings with beautiful formatting.
"""

import discord
import os
from typing import Optional, List, Tuple, Dict

from .data import Card, Spread, SpreadPosition
from .reading import Reading, ReadingResult
from .themes import get_theme_manager


# Color palette for embeds
COLORS = {
    "primary": 0x9B59B6,      # Mystic Purple
    "secondary": 0xE74C3C,    # Reversed Red
    "major_arcana": 0xFFD700, # Gold
    "wands": 0xFF6B35,        # Fire Orange
    "cups": 0x4ECDC4,         # Water Teal
    "swords": 0x95A5A6,       # Air Silver
    "pentacles": 0x27AE60,    # Earth Green
    "info": 0x3498DB,         # Info Blue
    "success": 0x2ECC71,      # Success Green
    "warning": 0xF39C12,      # Warning Orange
    "dark": 0x2C3E50,         # Dark background
}

SUIT_EMOJIS = {
    "MAJOR": "⭐",
    "WANDS": "🔥",
    "CUPS": "💧",
    "SWORDS": "⚔️",
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


def get_card_image_path(card: Card, reversed: bool = False) -> Optional[str]:
    """Get the path to a card image."""
    # Check themes directory for card image
    suit_lower = card.suit.name.lower()
    
    if card.is_major:
        filename = f"major_{card.number:02d}.png"
    else:
        if card.is_court:
            court_names = {11: "page", 12: "knight", 13: "queen", 14: "king"}
            filename = f"{suit_lower}_{card.number:02d}_{court_names.get(card.number, card.number)}.png"
        else:
            filename = f"{suit_lower}_{card.number:02d}.png"
    
    # Check multiple locations
    possible_paths = [
        f"themes/default/{filename}",
        f"themes/classic/{filename}",
        f"assets/cards/{filename}",
        f"/opt/astra-assets/themes/{filename}",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None


def create_reading_embed_with_images(
    reading: Reading,
    user: discord.User,
    spread: Spread,
    user_id: str
) -> Tuple[discord.Embed, List[discord.File]]:
    """
    Create reading embed with card images.
    
    Returns (embed, files) tuple. Files should be sent with the embed.
    """
    # Main embed
    embed = discord.Embed(
        title=f"🔮 {spread.name}",
        description=f"*{spread.description}*\n\n✨ {spread.num_cards} cards drawn for you...",
        color=COLORS["primary"],
        timestamp=reading.timestamp
    )
    
    # Question if provided
    if reading.question:
        embed.add_field(
            name="🌙 Your Question",
            value=f"> *{reading.question[:200]}*" + ("..." if len(reading.question) > 200 else ""),
            inline=False
        )
    
    # Collect image files
    files = []
    image_urls = []
    
    for i, result in enumerate(reading.results):
        position = spread.positions[i] if i < len(spread.positions) else None
        
        # Get card image
        image_path = get_card_image_path(result.card, result.reversed)
        if image_path and os.path.exists(image_path):
            # Create file attachment
            filename = f"card_{i+1}.png"
            files.append(discord.File(image_path, filename=filename))
            image_urls.append(f"attachment://{filename}")
        else:
            image_urls.append(None)
    
    # Set main image (first card)
    if image_urls and image_urls[0]:
        embed.set_image(url=image_urls[0])
    
    # Cards section
    for i, result in enumerate(reading.results):
        position = spread.positions[i] if i < len(spread.positions) else None
        
        emoji = POSITION_EMOJIS[result.position - 1] if result.position <= len(POSITION_EMOJIS) else "🃏"
        suit_emoji = get_suit_emoji(result.card)
        card_name = result.card.get_display_name(reversed=result.reversed)
        
        position_title = f"{emoji} **{position.name}**" if position else f"{emoji} Card {result.position}"
        card_subtitle = f"{suit_emoji} {card_name}"
        
        # Add image reference if available
        if image_urls[i]:
            card_subtitle += f"\n📎 See image above"
        
        value_parts = []
        if position:
            value_parts.append(f"*{position.meaning}*")
        
        keywords = result.get_keywords()
        if keywords:
            keyword_str = " • ".join(f"`{k}`" for k in keywords[:5])
            value_parts.append(f"\n**Keywords:** {keyword_str}")
        
        interpretation = result.get_interpretation()
        if len(interpretation) > 200:
            interpretation = interpretation[:197] + "..."
        value_parts.append(f"\n{interpretation}")
        
        embed.add_field(
            name=f"{position_title}\n{card_subtitle}",
            value="\n".join(value_parts),
            inline=False
        )
    
    # Summary
    summary = _create_reading_summary(reading, spread)
    if summary:
        embed.add_field(name="✨ Reading Insights", value=summary, inline=False)
    
    # Footer
    footer_text = f"Reading for {user.display_name} • {spread.num_cards} cards"
    embed.set_footer(
        text=footer_text,
        icon_url=user.display_avatar.url if user.display_avatar else None
    )
    
    return embed, files


def create_reading_embed(
    reading: Reading,
    user: discord.User,
    spread: Spread
) -> discord.Embed:
    """
    Create the main reading result embed with polished formatting.
    """
    # Main embed with spread color
    embed = discord.Embed(
        title=f"🔮 {spread.name}",
        description=f"*{spread.description}*\n\n✨ {spread.num_cards} cards drawn • Take a moment to reflect...",
        color=COLORS["primary"],
        timestamp=reading.timestamp
    )
    
    # Question if provided
    if reading.question:
        embed.add_field(
            name="🌙 Your Question",
            value=f"> *{reading.question[:200]}*" + ("..." if len(reading.question) > 200 else ""),
            inline=False
        )
    
    # Cards section
    for i, result in enumerate(reading.results):
        position = spread.positions[i] if i < len(spread.positions) else None
        
        # Card field with better formatting
        emoji = POSITION_EMOJIS[result.position - 1] if result.position <= len(POSITION_EMOJIS) else "🃏"
        suit_emoji = get_suit_emoji(result.card)
        card_name = result.card.get_display_name(reversed=result.reversed)
        
        # Position title
        position_title = f"{emoji} **{position.name}**" if position else f"{emoji} Card {result.position}"
        
        # Card subtitle
        card_subtitle = f"{suit_emoji} {card_name}"
        
        # Build value
        value_parts = []
        
        # Position meaning (italic, smaller)
        if position:
            value_parts.append(f"*{position.meaning}*")
        
        # Keywords in a nice format
        keywords = result.get_keywords()
        if keywords:
            keyword_str = " • ".join(f"`{k}`" for k in keywords[:5])
            value_parts.append(f"\n**Keywords:** {keyword_str}")
        
        # Interpretation
        interpretation = result.get_interpretation()
        if len(interpretation) > 250:
            interpretation = interpretation[:247] + "..."
        value_parts.append(f"\n{interpretation}")
        
        field_value = "\n".join(value_parts)
        
        embed.add_field(
            name=f"{position_title}\n{card_subtitle}",
            value=field_value,
            inline=False
        )
    
    # Reading summary - more concise
    summary = _create_reading_summary(reading, spread)
    if summary:
        embed.add_field(
            name="✨ Reading Insights",
            value=summary,
            inline=False
        )
    
    # Footer with reading stats
    footer_text = f"Reading for {user.display_name} • {spread.num_cards} cards • {reading.count_reversed()} reversed"
    embed.set_footer(
        text=footer_text,
        icon_url=user.display_avatar.url if user.display_avatar else None
    )
    
    return embed


def _create_reading_summary(reading: Reading, spread: Spread) -> str:
    """Create a concise summary interpretation of the reading."""
    lines = []
    
    # Elemental balance
    suit_counts = {}
    major_count = 0
    for result in reading.results:
        if result.card.is_major:
            major_count += 1
        else:
            suit = result.card.suit.name
            suit_counts[suit] = suit_counts.get(suit, 0) + 1
    
    # Dominant energy
    if major_count >= len(reading.results) / 2:
        lines.append("🌟 **Major Arcana present** — Significant spiritual forces at work")
    elif suit_counts:
        dominant_suit = max(suit_counts, key=suit_counts.get)
        suit_messages = {
            "WANDS": "🔥 **Fire energy** — Action, creativity, and passion drive this situation",
            "CUPS": "💧 **Water energy** — Emotions, relationships, and intuition are central",
            "SWORDS": "⚔️ **Air energy** — Intellect, decisions, and clarity matter most",
            "PENTACLES": "🌍 **Earth energy** — Material concerns and practical matters are the focus",
        }
        if dominant_suit in suit_messages:
            lines.append(suit_messages[dominant_suit])
    
    # Reversed cards note
    reversed_count = reading.count_reversed()
    if reversed_count > len(reading.results) / 2:
        lines.append("\n🔄 Many reversed cards suggest blocked or internal energies to address")
    elif reversed_count == 0 and len(reading.results) >= 3:
        lines.append("\n✨ Clear forward energy — the path is relatively unobstructed")
    
    return "\n".join(lines) if lines else ""


def create_spread_info_embed() -> discord.Embed:
    """Create an embed showing all available spreads."""
    from .data import SPREADS, SPREAD_DISPLAY_ORDER
    
    embed = discord.Embed(
        title="🔮 Available Tarot Spreads",
        description="Choose the spread that resonates with your question.",
        color=COLORS["info"]
    )
    
    for spread_key in SPREAD_DISPLAY_ORDER:
        spread = SPREADS[spread_key]
        
        emoji = "⭐" if spread.difficulty == "Beginner" else "🌙" if spread.difficulty == "Intermediate" else "✨"
        
        value = f"*{spread.description[:60]}...*\n" if len(spread.description) > 60 else f"*{spread.description}*\n"
        value += f"📊 {spread.num_cards} cards • ⏱️ ~{spread.estimated_time} • 📈 {spread.difficulty}"
        
        embed.add_field(
            name=f"{emoji} {spread.name}",
            value=value,
            inline=True
        )
    
    embed.set_footer(text="Astra serves one seeker at a time 🌙")
    return embed


def create_help_embed() -> discord.Embed:
    """Create the help embed."""
    embed = discord.Embed(
        title="🔮 Astra - Tarot Reading Bot",
        description="Welcome, seeker. I am Astra, your guide through the mysteries of the tarot.",
        color=COLORS["primary"]
    )
    
    embed.add_field(
        name="📖 Reading Commands",
        value=(
            "`/tarot-single` — Quick single card\n"
            "`/tarot-three` — Past, Present, Future\n"
            "`/tarot-celtic` — Full Celtic Cross (10 cards)\n"
            "`/tarot-relationship` — Relationship insights\n"
            "`/tarot-career` — Career guidance"
        ),
        inline=False
    )
    
    embed.add_field(
        name="📔 Journal Commands",
        value=(
            "`/tarot-journal` — View your saved readings\n"
            "`/tarot-save` — Save this reading to your journal"
        ),
        inline=False
    )
    
    embed.add_field(
        name="🎨 Theme Commands",
        value=(
            "`/tarot-theme` — Change your card deck\n"
            "`/tarot-themes` — Browse available decks"
        ),
        inline=False
    )
    
    embed.add_field(
        name="✨ Tips",
        value=(
            "• Take time to contemplate each card\n"
            "• Trust your intuition about meanings\n"
            "• The future is not fixed — use as guidance\n"
            "• Save readings to your journal for reflection"
        ),
        inline=False
    )
    
    embed.set_footer(text="May the stars guide your path 🌟")
    return embed


def create_journal_embed(readings: list, user: discord.User, page: int = 1, per_page: int = 5) -> discord.Embed:
    """Create embed showing user's saved readings."""
    embed = discord.Embed(
        title="📔 Your Tarot Journal",
        description=f"Personal readings for {user.display_name}",
        color=COLORS["info"]
    )
    
    if not readings:
        embed.description += "\n\n*Your journal is empty. Save readings with the Save button after a reading!*"
        return embed
    
    # Calculate pagination
    total_pages = (len(readings) + per_page - 1) // per_page
    start = (page - 1) * per_page
    end = start + per_page
    page_readings = readings[start:end]
    
    for i, entry in enumerate(page_readings, start + 1):
        # Handle both JournalEntry objects and dicts
        if hasattr(entry, 'to_dict'):
            entry_data = entry.to_dict()
        elif hasattr(entry, '__dict__'):
            entry_data = entry.__dict__
        else:
            entry_data = entry
        
        date_str = entry_data.get('timestamp', 'Unknown date')[:10] if isinstance(entry_data, dict) else str(entry_data.timestamp)[:10]
        spread = entry_data.get('spread_type', 'Unknown spread') if isinstance(entry_data, dict) else entry_data.spread_type
        question = entry_data.get('question', '') if isinstance(entry_data, dict) else entry_data.question
        cards = entry_data.get('cards', []) if isinstance(entry_data, dict) else entry_data.cards
        
        card_names = []
        for c in cards[:3]:
            if isinstance(c, dict):
                card_names.append(c.get('name', 'Unknown'))
            else:
                card_names.append(str(c))
        cards_str = ", ".join(card_names)
        if len(cards) > 3:
            cards_str += f" +{len(cards) - 3} more"
        
        value = f"📊 {spread} • 🃏 {cards_str}"
        if question:
            value += f"\n🌙 *{question[:60]}...*" if len(question) > 60 else f"\n🌙 *{question}*"
        
        embed.add_field(
            name=f"#{i} • {date_str}",
            value=value,
            inline=False
        )
    
    embed.set_footer(text=f"Page {page}/{max(1, total_pages)} • {len(readings)} total readings 🌙")
    return embed


def create_journal_entry_embed(entry, user: discord.User) -> discord.Embed:
    """Create detailed embed for a single journal entry."""
    # Handle both JournalEntry objects and dicts
    if hasattr(entry, 'to_dict'):
        entry_data = entry.to_dict()
    elif hasattr(entry, '__dict__'):
        entry_data = entry.__dict__
    else:
        entry_data = entry
    
    is_dict = isinstance(entry_data, dict)
    
    spread_type = entry_data.get('spread_type', 'Reading') if is_dict else entry_data.spread_type
    question = entry_data.get('question') if is_dict else entry_data.question
    cards = entry_data.get('cards', []) if is_dict else entry_data.cards
    date_str = entry_data.get('timestamp', 'Unknown date') if is_dict else str(entry_data.timestamp)
    
    embed = discord.Embed(
        title=f"📔 Journal Entry • {spread_type}",
        description=f"Saved on {date_str}",
        color=COLORS["primary"]
    )
    
    if question:
        embed.add_field(
            name="🌙 Question",
            value=f"*{question}*",
            inline=False
        )
    
    for card in cards:
        if isinstance(card, dict):
            card_name = card.get('name', 'Unknown')
            position = card.get('position', 0)
            is_reversed = card.get('reversed', False)
            meaning = card.get('meaning', '')
        else:
            card_name = str(getattr(card, 'name', 'Unknown'))
            position = getattr(card, 'position', 0)
            is_reversed = getattr(card, 'reversed', False)
            meaning = str(getattr(card, 'meaning', ''))
        
        emoji = POSITION_EMOJIS[position - 1] if position <= len(POSITION_EMOJIS) else "🃏"
        status = " (Reversed)" if is_reversed else ""
        
        embed.add_field(
            name=f"{emoji} {card_name}{status}",
            value=meaning[:200] + "..." if len(meaning) > 200 else meaning,
            inline=False
        )
    
    embed.set_footer(text=f"Reading for {user.display_name} 🌟")
    return embed


def create_save_confirmation_embed(reading: Reading) -> discord.Embed:
    """Create confirmation when reading is saved."""
    embed = discord.Embed(
        title="📔 Reading Saved",
        description="This reading has been added to your personal journal.",
        color=COLORS["success"]
    )
    
    embed.add_field(
        name="Details",
        value=(
            f"📊 {reading.spread_type}\n"
            f"🃏 {len(reading.results)} cards\n"
            f"🕐 {reading.timestamp.strftime('%Y-%m-%d %H:%M')}"
        ),
        inline=False
    )
    
    embed.set_footer(text="View your journal with /tarot-journal 🌙")
    return embed


def create_theme_selection_embed(
    themes: List,
    user_name: str,
    is_first_time: bool = False
) -> discord.Embed:
    """Create the theme selection embed."""
    if is_first_time:
        title = "🎨 Welcome to Astra!"
        description = f"Hello {user_name}! Choose a deck that speaks to you."
    else:
        title = "🎨 Select Your Deck"
        description = "Choose a tarot deck theme for your readings."
    
    embed = discord.Embed(
        title=title,
        description=description,
        color=COLORS["primary"]
    )
    
    for i, theme in enumerate(themes[:10], 1):
        emoji = "⭐" if theme.is_default else "🃏"
        desc = theme.description[:80] + "..." if len(theme.description) > 80 else theme.description
        
        embed.add_field(
            name=f"{emoji} {i}. {theme.name}",
            value=f"*{desc}*",
            inline=True
        )
    
    return embed


def create_theme_selected_embed(theme, user_name: str) -> discord.Embed:
    """Confirmation embed when a user selects a theme."""
    embed = discord.Embed(
        title="✅ Deck Selected",
        description=f"**{user_name}**, you've chosen **{theme.name}**!",
        color=COLORS["success"]
    )
    
    embed.add_field(
        name="About This Deck",
        value=theme.description,
        inline=False
    )
    
    embed.set_footer(text="Ready to begin? Use /tarot-single 🔮")
    return embed
