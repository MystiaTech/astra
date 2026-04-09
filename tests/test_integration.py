"""
Integration Tests
=================
QA: Chloe

End-to-end tests for complete reading flows.
"""

import pytest


class TestCompleteReadingFlow:
    """Test complete user journeys."""
    
    def test_single_card_reading_flow(self):
        """FLOW-001: Complete single card reading works end-to-end."""
        from astra.data import SPREADS, TAROT_DECK
        from astra.reading import Reading, ReadingResult
        import random
        
        # Simulate drawing a card
        spread = SPREADS["single"]
        card = random.choice(TAROT_DECK)
        
        reading = Reading(
            spread_type="single",
            question="What should I focus on today?",
            results=[ReadingResult(card=card, position=1, reversed=False)]
        )
        
        # Verify reading structure
        assert len(reading.results) == 1
        assert reading.question is not None
        assert reading.results[0].card is not None
    
    def test_three_card_reading_has_coherent_narrative(self):
        """FLOW-002: Three card reading should have Past-Present-Future flow."""
        from astra.data import SPREADS
        from astra.bot import TarotCommands
        
        cog = TarotCommands(None)
        reading = cog._draw_cards(
            spread_type="three",
            question="How will my week go?",
            allow_reversed=False
        )
        
        spread = SPREADS["three"]
        
        # Verify we have all three time periods
        assert len(reading.results) == 3
        
        # Position names should tell a story
        position_names = [p.name for p in spread.positions]
        assert any("Past" in n for n in position_names), "Should reference past"
        assert any("Present" in n or "Current" in n for n in position_names), \
            "Should reference present"
        assert any("Future" in n for n in position_names), "Should reference future"


class TestEmbedGeneration:
    """Test Discord embed generation."""
    
    def test_reading_embed_has_required_fields(self):
        """EMBED-001: Reading embed must have all required components."""
        from astra.embeds import create_reading_embed
        from astra.reading import Reading, ReadingResult
        from astra.data import TAROT_DECK, SPREADS
        from unittest.mock import MagicMock
        
        # Create a test reading
        reading = Reading(
            spread_type="single",
            question="Test question",
            results=[ReadingResult(card=TAROT_DECK[0], position=1, reversed=False)]
        )
        
        # Create mock user
        mock_user = MagicMock()
        mock_user.display_name = "TestUser"
        mock_user.display_avatar = MagicMock()
        mock_user.display_avatar.url = "http://example.com/avatar.png"
        
        spread = SPREADS["single"]
        
        embed = create_reading_embed(reading, mock_user, spread)
        
        # Verify embed structure
        assert embed.title is not None
        assert len(embed.fields) > 0
        assert embed.timestamp is not None
        assert embed.footer is not None


class TestDataConsistency:
    """Test consistency across data modules."""
    
    def test_all_spread_cards_reference_valid_cards(self):
        """CONSISTENCY-001: Card references in code should be valid."""
        from astra.data import TAROT_DECK, CardSuit
        
        # Verify we can access all card types
        major = [c for c in TAROT_DECK if c.suit == CardSuit.MAJOR]
        wands = [c for c in TAROT_DECK if c.suit == CardSuit.WANDS]
        cups = [c for c in TAROT_DECK if c.suit == CardSuit.CUPS]
        swords = [c for c in TAROT_DECK if c.suit == CardSuit.SWORDS]
        pentacles = [c for c in TAROT_DECK if c.suit == CardSuit.PENTACLES]
        
        assert len(major) == 22
        assert len(wands) == 14
        assert len(cups) == 14
        assert len(swords) == 14
        assert len(pentacles) == 14
    
    def test_image_placeholders_follow_convention(self):
        """CONSISTENCY-002: Image placeholders should follow naming convention."""
        from astra.data import TAROT_DECK
        
        for card in TAROT_DECK:
            placeholder = card.image_placeholder
            
            # Should be PNG
            assert placeholder.endswith('.png'), \
                f"{card.name} placeholder should be PNG"
            
            # Should follow naming pattern
            parts = placeholder.replace('.png', '').split('_')
            assert len(parts) >= 2, \
                f"{card.name} placeholder should have multiple parts"


class TestPerformance:
    """Test performance characteristics."""
    
    def test_card_drawing_is_fast(self):
        """PERF-001: Drawing cards should be fast."""
        from astra.bot import TarotCommands
        import time
        
        cog = TarotCommands(None)
        
        # Time drawing multiple Celtic Cross readings
        start = time.time()
        for _ in range(100):
            cog._draw_cards("celtic", "Test", True)
        elapsed = time.time() - start
        
        # Should complete 100 readings in under 1 second
        assert elapsed < 1.0, f"Card drawing too slow: {elapsed}s for 100 draws"


class TestSecurity:
    """Test security considerations."""
    
    def test_no_sensitive_data_in_card_data(self):
        """SEC-001: Card data should not contain sensitive information."""
        from astra.data import TAROT_DECK
        
        sensitive_patterns = ['password', 'secret', 'key', 'token', 'admin']
        
        for card in TAROT_DECK:
            all_text = f"{card.name} {card.meaning} {card.meaning_reversed}"
            all_text_lower = all_text.lower()
            
            for pattern in sensitive_patterns:
                assert pattern not in all_text_lower, \
                    f"{card.name} may contain sensitive data pattern: {pattern}"
