"""
Astra Discord Bot - Backend Implementation
==========================================
IMPLEMENTATION BY: Emma (Backend Lead)

Core bot functionality with session management for single-user-at-a-time readings.
Uses discord.py with slash commands.
"""

import asyncio
import logging
import random
from datetime import datetime, timedelta
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from .data import TAROT_DECK, SPREADS, Card, Spread
from .reading import Reading, ReadingSession, ReadingResult
from .embeds import create_reading_embed, create_spread_info_embed, create_help_embed
from .themes import get_theme_manager
from .theme_commands import ThemeCommands, prompt_theme_selection

logger = logging.getLogger(__name__)


class AstraBot(commands.Bot):
    """
    Astra Tarot Reading Bot
    
    Features:
    - Slash commands for all interactions
    - Single-session reading management (one user at a time)
    - Multiple spread types
    - Rich embeds for card displays
    """
    
    def __init__(self):
        intents = discord.Intents.default()
        # Note: message_content intent not needed for slash commands only
        # Keeping it disabled avoids privileged intent requirements
        
        super().__init__(
            command_prefix="!",  # Fallback only, we use slash commands
            intents=intents,
            activity=discord.Activity(
                type=discord.ActivityType.watching,
                name="the stars align 🔮"
            ),
            status=discord.Status.online,
        )
        
        # Session management - only one active reading at a time
        self.active_session: Optional[ReadingSession] = None
        self.session_timeout: int = 300  # 5 minutes
        self.session_lock = asyncio.Lock()
        
        # Statistics
        self.readings_completed = 0
        self.start_time = datetime.now()
    
    async def setup_hook(self):
        """Set up the bot and sync commands."""
        logger.info("Setting up Astra bot...")
        
        # Initialize theme manager
        self.theme_manager = get_theme_manager(self)
        await self.theme_manager.scan_themes()
        self.theme_manager.start_watching()
        
        # Add command cogs
        await self.add_cog(TarotCommands(self))
        await self.add_cog(ThemeCommands(self))
        
        # Sync slash commands
        try:
            synced = await self.tree.sync()
            logger.info(f"Synced {len(synced)} slash commands")
        except Exception as e:
            logger.error(f"Failed to sync commands: {e}")
    
    async def on_ready(self):
        """Called when bot is ready."""
        logger.info(f"Astra is online! Logged in as {self.user} (ID: {self.user.id})")
        logger.info(f"Bot is in {len(self.guilds)} guilds")
    
    async def on_error(self, event_method: str, *args, **kwargs):
        """Handle errors."""
        logger.exception(f"Error in {event_method}")
    
    async def acquire_reading_session(
        self, 
        user: discord.User,
        spread_type: str
    ) -> Optional[ReadingSession]:
        """
        Attempt to acquire a reading session for a user.
        
        Returns None if another reading is in progress.
        """
        async with self.session_lock:
            # Check if there's an active session
            if self.active_session is not None:
                # Check if session expired
                if self.active_session.is_expired(self.session_timeout):
                    logger.info(f"Session for {self.active_session.user_id} expired, releasing")
                    self.active_session = None
                else:
                    # Session is active and valid
                    return None
            
            # Create new session
            session = ReadingSession(
                user_id=user.id,
                username=user.name,
                spread_type=spread_type,
                started_at=datetime.now(),
            )
            self.active_session = session
            logger.info(f"New session acquired by {user.name} for {spread_type}")
            return session
    
    async def release_reading_session(self, user_id: int) -> bool:
        """
        Release a reading session.
        
        Returns True if session was released, False if user didn't own it.
        """
        async with self.session_lock:
            if self.active_session and self.active_session.user_id == user_id:
                self.readings_completed += 1
                self.active_session = None
                logger.info(f"Session released by user {user_id}")
                return True
            return False
    
    def get_session_status(self) -> dict:
        """Get current session status for status display."""
        if self.active_session is None:
            return {"active": False, "user": None, "spread": None}
        
        return {
            "active": True,
            "user": self.active_session.username,
            "spread": self.active_session.spread_type,
            "elapsed": self.active_session.elapsed_seconds(),
        }
    
    async def close(self):
        """Clean up on shutdown."""
        if hasattr(self, 'theme_manager'):
            self.theme_manager.stop_watching()
        await super().close()


class TarotCommands(commands.Cog):
    """
    Tarot reading slash commands for Astra.
    
    IMPLEMENTED BY: Emma (Backend Lead)
    """
    
    def __init__(self, bot: AstraBot):
        self.bot = bot
    
    # ========================================================================
    # SLASH COMMAND: /tarot single
    # ========================================================================
    @app_commands.command(name="tarot-single", description="Draw a single card for quick guidance")
    @app_commands.describe(
        question="Optional: What would you like guidance on?",
        reversed_cards="Allow reversed cards in the reading?"
    )
    async def tarot_single(
        self,
        interaction: discord.Interaction,
        question: Optional[str] = None,
        reversed_cards: bool = True
    ):
        """Single card reading command."""
        await self._perform_reading(
            interaction=interaction,
            spread_type="single",
            question=question,
            allow_reversed=reversed_cards
        )
    
    # ========================================================================
    # SLASH COMMAND: /tarot three
    # ========================================================================
    @app_commands.command(name="tarot-three", description="Past, Present, Future three-card spread")
    @app_commands.describe(
        question="Optional: What would you like guidance on?",
        reversed_cards="Allow reversed cards in the reading?"
    )
    async def tarot_three(
        self,
        interaction: discord.Interaction,
        question: Optional[str] = None,
        reversed_cards: bool = True
    ):
        """Three-card spread command."""
        await self._perform_reading(
            interaction=interaction,
            spread_type="three",
            question=question,
            allow_reversed=reversed_cards
        )
    
    # ========================================================================
    # SLASH COMMAND: /tarot mind-body-spirit
    # ========================================================================
    @app_commands.command(name="tarot-mind-body-spirit", description="Holistic self-examination spread")
    @app_commands.describe(
        question="Optional: Focus area for the reading",
        reversed_cards="Allow reversed cards in the reading?"
    )
    async def tarot_mind_body_spirit(
        self,
        interaction: discord.Interaction,
        question: Optional[str] = None,
        reversed_cards: bool = True
    ):
        """Mind-Body-Spirit spread command."""
        await self._perform_reading(
            interaction=interaction,
            spread_type="mind_body_spirit",
            question=question,
            allow_reversed=reversed_cards
        )
    
    # ========================================================================
    # SLASH COMMAND: /tarot situation-action
    # ========================================================================
    @app_commands.command(name="tarot-situation-action", description="Problem-solving spread")
    @app_commands.describe(
        question="What situation would you like guidance on?",
        reversed_cards="Allow reversed cards in the reading?"
    )
    async def tarot_situation_action(
        self,
        interaction: discord.Interaction,
        question: str,
        reversed_cards: bool = True
    ):
        """Situation-Action-Outcome spread command."""
        await self._perform_reading(
            interaction=interaction,
            spread_type="situation_action",
            question=question,
            allow_reversed=reversed_cards
        )
    
    # ========================================================================
    # SLASH COMMAND: /tarot relationship
    # ========================================================================
    @app_commands.command(name="tarot-relationship", description="Seven-card relationship spread")
    @app_commands.describe(
        person="Name or description of the other person (optional)",
        reversed_cards="Allow reversed cards in the reading?"
    )
    async def tarot_relationship(
        self,
        interaction: discord.Interaction,
        person: Optional[str] = None,
        reversed_cards: bool = True
    ):
        """Relationship spread command."""
        question = f"Relationship with {person}" if person else "Relationship dynamics"
        await self._perform_reading(
            interaction=interaction,
            spread_type="relationship",
            question=question,
            allow_reversed=reversed_cards
        )
    
    # ========================================================================
    # SLASH COMMAND: /tarot career
    # ========================================================================
    @app_commands.command(name="tarot-career", description="Five-card career guidance spread")
    @app_commands.describe(
        focus="Career focus area (e.g., 'promotion', 'new job', 'skills')",
        reversed_cards="Allow reversed cards in the reading?"
    )
    async def tarot_career(
        self,
        interaction: discord.Interaction,
        focus: Optional[str] = None,
        reversed_cards: bool = True
    ):
        """Career path spread command."""
        question = f"Career focus: {focus}" if focus else "Career guidance"
        await self._perform_reading(
            interaction=interaction,
            spread_type="career",
            question=question,
            allow_reversed=reversed_cards
        )
    
    # ========================================================================
    # SLASH COMMAND: /tarot celtic
    # ========================================================================
    @app_commands.command(name="tarot-celtic", description="Full Celtic Cross (10 cards) - Advanced spread")
    @app_commands.describe(
        question="The situation or question for deep exploration",
        reversed_cards="Allow reversed cards in the reading?"
    )
    async def tarot_celtic(
        self,
        interaction: discord.Interaction,
        question: str,
        reversed_cards: bool = True
    ):
        """Celtic Cross spread command."""
        await self._perform_reading(
            interaction=interaction,
            spread_type="celtic",
            question=question,
            allow_reversed=reversed_cards
        )
    
    # ========================================================================
    # SLASH COMMAND: /tarot spreads
    # ========================================================================
    @app_commands.command(name="tarot-spreads", description="Learn about available tarot spreads")
    async def tarot_spreads(self, interaction: discord.Interaction):
        """Show information about all available spreads."""
        embed = create_spread_info_embed()
        await interaction.response.send_message(embed=embed)
    
    # ========================================================================
    # SLASH COMMAND: /tarot help
    # ========================================================================
    @app_commands.command(name="tarot-help", description="Get help with Astra tarot readings")
    async def tarot_help(self, interaction: discord.Interaction):
        """Show help information."""
        embed = create_help_embed()
        await interaction.response.send_message(embed=embed, ephemeral=True)
    
    # ========================================================================
    # SLASH COMMAND: /tarot cancel
    # ========================================================================
    @app_commands.command(name="tarot-cancel", description="Cancel your current reading session")
    async def tarot_cancel(self, interaction: discord.Interaction):
        """Cancel the user's current reading session."""
        released = await self.bot.release_reading_session(interaction.user.id)
        
        if released:
            await interaction.response.send_message(
                "🔮 Your reading session has been cancelled. The stars thank you for your visit.",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "You don't have an active reading session to cancel.",
                ephemeral=True
            )
    
    # ========================================================================
    # CORE READING LOGIC
    # ========================================================================
    
    async def _perform_reading(
        self,
        interaction: discord.Interaction,
        spread_type: str,
        question: Optional[str],
        allow_reversed: bool
    ):
        """
        Core reading logic - handles session management and card drawing.
        
        This ensures only one user has an active reading at a time.
        """
        # Check if user has selected a theme (first time only)
        if not self.bot.theme_manager.has_selected_theme(interaction.user.id):
            # Show theme selection first
            from .theme_commands import prompt_theme_selection
            theme_selected = await prompt_theme_selection(self.bot, interaction)
            if not theme_selected:
                return
            # Re-defer for the actual reading
            await interaction.response.defer(thinking=True)
        else:
            # Defer response since reading might take a moment
            await interaction.response.defer(thinking=True)
        
        # Try to acquire session
        session = await self.bot.acquire_reading_session(
            user=interaction.user,
            spread_type=spread_type
        )
        
        if session is None:
            # Someone else is reading
            status = self.bot.get_session_status()
            await interaction.followup.send(
                embed=discord.Embed(
                    title="🔮 Astra is Currently With Another Seeker",
                    description=(
                        f"**{status['user']}** is currently receiving a reading.\n\n"
                        f"Astra serves one seeker at a time to ensure each reading "
                        f"receives her full attention and energy.\n\n"
                        f"Please try again in a few moments when the current reading completes."
                    ),
                    color=0x9B59B6
                ).set_footer(text="The stars teach patience 🌙")
            )
            return
        
        try:
            # Perform the reading
            reading = self._draw_cards(
                spread_type=spread_type,
                question=question,
                allow_reversed=allow_reversed
            )
            
            # Create and send the reading embed
            embed = create_reading_embed(
                reading=reading,
                user=interaction.user,
                spread=SPREADS[spread_type]
            )
            
            await interaction.followup.send(embed=embed)
            
            # Release session after a short delay to allow reading
            await asyncio.sleep(2)
            await self.bot.release_reading_session(interaction.user.id)
            
        except Exception as e:
            logger.exception("Error performing reading")
            await self.bot.release_reading_session(interaction.user.id)
            await interaction.followup.send(
                "🔮 The mists cloud my vision. Please try again in a moment.",
                ephemeral=True
            )
    
    def _draw_cards(
        self,
        spread_type: str,
        question: Optional[str],
        allow_reversed: bool
    ) -> Reading:
        """
        Draw cards for a reading.
        
        Uses proper shuffling and randomization.
        """
        spread = SPREADS[spread_type]
        
        # Shuffle deck
        shuffled = random.sample(TAROT_DECK, len(TAROT_DECK))
        
        # Draw required number of cards
        drawn_cards = shuffled[:spread.num_cards]
        
        # Determine orientation for each card
        results = []
        for i, card in enumerate(drawn_cards):
            is_reversed = allow_reversed and random.choice([True, False])
            results.append(ReadingResult(
                card=card,
                position=i + 1,
                reversed=is_reversed
            ))
        
        return Reading(
            spread_type=spread_type,
            question=question,
            results=results,
            timestamp=datetime.now()
        )
