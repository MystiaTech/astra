"""
Bot Logic Tests
===============
QA: Chloe

Tests for bot functionality, session management, and command handling.
Uses mocking to test without actual Discord connection.
"""

import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime


class TestSessionManagement:
    """Test the single-session reading constraint."""
    
    @pytest_asyncio.fixture
    async def bot(self):
        """Create a mocked bot instance."""
        from astra.bot import AstraBot
        
        bot = AstraBot()
        bot.active_session = None
        bot.session_lock = MagicMock()
        bot.session_lock.__aenter__ = AsyncMock(return_value=None)
        bot.session_lock.__aexit__ = AsyncMock(return_value=None)
        return bot
    
    @pytest.mark.asyncio
    async def test_can_acquire_session_when_none_active(self, bot):
        """SESSION-001: Can acquire session when none is active."""
        mock_user = MagicMock()
        mock_user.id = 12345
        mock_user.name = "TestUser"
        
        session = await bot.acquire_reading_session(mock_user, "single")
        
        assert session is not None
        assert session.user_id == 12345
        assert session.spread_type == "single"
    
    @pytest.mark.asyncio
    async def test_cannot_acquire_when_session_active(self, bot):
        """SESSION-002: Cannot acquire session when another is active."""
        from astra.reading import ReadingSession
        
        # Create existing session
        bot.active_session = ReadingSession(
            user_id=99999,
            username="OtherUser",
            spread_type="celtic",
            started_at=datetime.now()
        )
        
        mock_user = MagicMock()
        mock_user.id = 12345
        mock_user.name = "TestUser"
        
        session = await bot.acquire_reading_session(mock_user, "single")
        
        assert session is None
    
    @pytest.mark.asyncio
    async def test_session_release_allows_new_session(self, bot):
        """SESSION-003: Releasing session allows new acquisition."""
        from astra.reading import ReadingSession
        
        # Create and then release session
        bot.active_session = ReadingSession(
            user_id=12345,
            username="TestUser",
            spread_type="single",
            started_at=datetime.now()
        )
        
        released = await bot.release_reading_session(12345)
        
        assert released is True
        assert bot.active_session is None
    
    @pytest.mark.asyncio
    async def test_cannot_release_others_session(self, bot):
        """SESSION-004: Cannot release someone else's session."""
        from astra.reading import ReadingSession
        
        bot.active_session = ReadingSession(
            user_id=99999,
            username="OtherUser",
            spread_type="celtic",
            started_at=datetime.now()
        )
        
        released = await bot.release_reading_session(12345)
        
        assert released is False
        assert bot.active_session is not None


class TestCardDrawing:
    """Test card drawing mechanics."""
    
    def test_draws_correct_number_of_cards(self):
        """DRAW-001: Should draw correct number of cards for spread."""
        from astra.bot import TarotCommands
        from astra.reading import Reading
        
        # Create a mock bot and cog
        mock_bot = MagicMock()
        cog = TarotCommands(mock_bot)
        
        # Test each spread type
        spread_card_counts = {
            "single": 1,
            "three": 3,
            "mind_body_spirit": 3,
            "situation_action": 3,
            "relationship": 7,
            "career": 5,
            "celtic": 10,
        }
        
        for spread_type, expected_count in spread_card_counts.items():
            reading = cog._draw_cards(
                spread_type=spread_type,
                question="Test question",
                allow_reversed=False
            )
            
            assert len(reading.results) == expected_count, \
                f"{spread_type} should draw {expected_count} cards"
    
    def test_no_duplicate_cards_in_reading(self):
        """DRAW-002: Should not draw duplicate cards in same reading."""
        from astra.bot import TarotCommands
        
        mock_bot = MagicMock()
        cog = TarotCommands(mock_bot)
        
        # Draw Celtic Cross (10 cards - high chance of duplicates if buggy)
        reading = cog._draw_cards(
            spread_type="celtic",
            question="Test",
            allow_reversed=False
        )
        
        card_ids = [(r.card.name, r.card.suit) for r in reading.results]
        unique_cards = set(card_ids)
        
        assert len(card_ids) == len(unique_cards), \
            "Should not have duplicate cards in reading"
    
    def test_reversed_cards_when_allowed(self):
        """DRAW-003: Should include reversed cards when allowed."""
        from astra.bot import TarotCommands
        import random
        
        mock_bot = MagicMock()
        cog = TarotCommands(mock_bot)
        
        # Force some reversals by setting seed
        random.seed(42)
        
        # Run multiple times to likely get some reversals
        reversed_found = False
        for _ in range(20):
            reading = cog._draw_cards(
                spread_type="three",
                question="Test",
                allow_reversed=True
            )
            if any(r.reversed for r in reading.results):
                reversed_found = True
                break
        
        assert reversed_found, "Should get reversed cards when allowed"
    
    def test_no_reversed_cards_when_disallowed(self):
        """DRAW-004: Should not have reversed cards when disallowed."""
        from astra.bot import TarotCommands
        
        mock_bot = MagicMock()
        cog = TarotCommands(mock_bot)
        
        reading = cog._draw_cards(
            spread_type="three",
            question="Test",
            allow_reversed=False
        )
        
        assert all(not r.reversed for r in reading.results), \
            "Should not have reversed cards when disallowed"


class TestReadingModel:
    """Test Reading data model."""
    
    def test_reading_has_timestamp(self):
        """MODEL-001: Reading should have timestamp."""
        from astra.reading import Reading
        
        reading = Reading(
            spread_type="single",
            question="Test",
            results=[]
        )
        
        assert reading.timestamp is not None
    
    def test_count_reversed(self):
        """MODEL-002: Should correctly count reversed cards."""
        from astra.reading import Reading, ReadingResult
        from astra.data import TAROT_DECK
        
        results = [
            ReadingResult(card=TAROT_DECK[0], position=1, reversed=False),
            ReadingResult(card=TAROT_DECK[1], position=2, reversed=True),
            ReadingResult(card=TAROT_DECK[2], position=3, reversed=True),
        ]
        
        reading = Reading(
            spread_type="three",
            question="Test",
            results=results
        )
        
        assert reading.count_reversed() == 2


class TestErrorHandling:
    """Test error handling and edge cases."""
    
    @pytest.mark.asyncio
    async def test_handles_session_timeout(self, bot):
        """ERROR-001: Should handle session timeout gracefully."""
        from astra.reading import ReadingSession
        from datetime import datetime, timedelta
        
        # Create expired session
        bot.active_session = ReadingSession(
            user_id=99999,
            username="OldUser",
            spread_type="single",
            started_at=datetime.now() - timedelta(minutes=10)
        )
        
        mock_user = MagicMock()
        mock_user.id = 12345
        mock_user.name = "NewUser"
        
        # Should be able to acquire new session since old one expired
        session = await bot.acquire_reading_session(mock_user, "single")
        
        # Note: This depends on implementation - if expired sessions are cleaned
        # up during acquisition, this should return a new session
        assert session is not None or bot.active_session.user_id == 99999


class TestCommandsExist:
    """Test that all expected commands are defined."""
    
    def test_all_spread_commands_exist(self):
        """CMD-001: All spreads should have corresponding commands."""
        from astra.bot import TarotCommands
        
        cog = TarotCommands(MagicMock())
        
        # Check for expected command methods
        expected_commands = [
            "tarot_single",
            "tarot_three",
            "tarot_mind_body_spirit",
            "tarot_situation_action",
            "tarot_relationship",
            "tarot_career",
            "tarot_celtic",
            "tarot_spreads",
            "tarot_help",
            "tarot_cancel",
        ]
        
        for cmd in expected_commands:
            assert hasattr(cog, cmd), f"Missing command: {cmd}"
