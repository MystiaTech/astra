"""
Spread Tests
============
QA: Chloe

Validates tarot spread definitions and structures.
"""

import pytest
from astra.data import SPREADS, Spread


class TestSpreadRegistry:
    """Verify spread registry has all spreads."""
    
    def test_all_spreads_exist(self, sample_spreads):
        """SPREAD-REG-001: All expected spreads must be registered."""
        expected_spreads = [
            "single",
            "three",
            "mind_body_spirit",
            "situation_action",
            "celtic",
            "relationship",
            "career",
        ]
        
        for spread_key in expected_spreads:
            assert spread_key in sample_spreads, f"Missing spread: {spread_key}"
    
    def test_spreads_have_required_attributes(self, sample_spreads):
        """SPREAD-REG-002: Each spread must have all required attributes."""
        for key, spread in sample_spreads.items():
            assert spread.name, f"{key} missing name"
            assert spread.description, f"{key} missing description"
            assert spread.num_cards > 0, f"{key} must have cards"
            assert spread.positions, f"{key} must have positions"
            assert len(spread.positions) == spread.num_cards, \
                f"{key} positions count mismatch"
            assert spread.best_for, f"{key} should list best uses"
            assert spread.difficulty in ["Beginner", "Intermediate", "Advanced"], \
                f"{key} has invalid difficulty"


class TestSingleCardSpread:
    """Test the single card spread."""
    
    def test_single_has_one_card(self, sample_spreads):
        """SINGLE-001: Single card spread must have exactly 1 card."""
        spread = sample_spreads["single"]
        assert spread.num_cards == 1
        assert len(spread.positions) == 1
    
    def test_single_position_is_message(self, sample_spreads):
        """SINGLE-002: Position should be 'The Message'."""
        spread = sample_spreads["single"]
        assert spread.positions[0].name == "The Message"


class TestThreeCardSpreads:
    """Test three-card spreads."""
    
    def test_three_card_has_three_cards(self, sample_spreads):
        """THREE-001: Three card spread must have exactly 3 cards."""
        spread = sample_spreads["three"]
        assert spread.num_cards == 3
        assert len(spread.positions) == 3
    
    def test_three_card_positions(self, sample_spreads):
        """THREE-002: Positions should be Past, Present, Future."""
        spread = sample_spreads["three"]
        names = [p.name for p in spread.positions]
        assert "Past" in names, "Should have Past position"
        assert "Present" in names or "Current" in str(names), "Should have Present position"
        assert "Future" in names or "Outcome" in names, "Should have Future position"


class TestCelticCross:
    """Test the Celtic Cross spread."""
    
    def test_celtic_has_ten_cards(self, sample_spreads):
        """CELTIC-001: Celtic Cross must have exactly 10 cards."""
        spread = sample_spreads["celtic"]
        assert spread.num_cards == 10
        assert len(spread.positions) == 10
    
    def test_celtic_is_advanced(self, sample_spreads):
        """CELTIC-002: Celtic Cross should be marked as Advanced."""
        spread = sample_spreads["celtic"]
        assert spread.difficulty == "Advanced"
    
    def test_celtic_has_traditional_positions(self, sample_spreads):
        """CELTIC-003: Should have traditional Celtic Cross positions."""
        spread = sample_spreads["celtic"]
        names = [p.name for p in spread.positions]
        
        # Key positions that should exist
        assert any("Present" in n or "Situation" in n for n in names), \
            "Should have present situation"
        assert any("Challenge" in n or "Cross" in n for n in names), \
            "Should have challenge/cross"
        assert any("Foundation" in n or "Root" in n for n in names), \
            "Should have foundation"
        assert any("Future" in n or "Outcome" in n for n in names), \
            "Should have outcome"


class TestRelationshipSpread:
    """Test the relationship spread."""
    
    def test_relationship_has_seven_cards(self, sample_spreads):
        """REL-001: Relationship spread must have exactly 7 cards."""
        spread = sample_spreads["relationship"]
        assert spread.num_cards == 7
        assert len(spread.positions) == 7
    
    def test_relationship_has_self_and_other(self, sample_spreads):
        """REL-002: Should have positions for self and other person."""
        spread = sample_spreads["relationship"]
        names = [p.name.lower() for p in spread.positions]
        
        assert any("you" in n or "self" in n for n in names), \
            "Should have self position"
        assert any("other" in n or "partner" in n for n in names), \
            "Should have other person position"


class TestCareerSpread:
    """Test the career spread."""
    
    def test_career_has_five_cards(self, sample_spreads):
        """CAREER-001: Career spread must have exactly 5 cards."""
        spread = sample_spreads["career"]
        assert spread.num_cards == 5
        assert len(spread.positions) == 5
    
    def test_career_has_professional_focus(self, sample_spreads):
        """CAREER-002: Should have career-relevant positions."""
        spread = sample_spreads["career"]
        combined = " ".join([p.name.lower() for p in spread.positions])
        
        career_terms = ["career", "work", "position", "skill", "opportunit", "challenge"]
        assert any(term in combined for term in career_terms), \
            "Should have career-related position names"


class TestSpreadDocumentation:
    """Test spread documentation quality."""
    
    def test_all_positions_have_descriptions(self, sample_spreads):
        """DOC-001: Every position must have a description."""
        for key, spread in sample_spreads.items():
            for i, pos in enumerate(spread.positions):
                assert pos.description, f"{key} position {i+1} missing description"
                assert len(pos.description) > 20, \
                    f"{key} position {i+1} description too short"
    
    def test_all_positions_have_meanings(self, sample_spreads):
        """DOC-002: Every position must have a meaning summary."""
        for key, spread in sample_spreads.items():
            for i, pos in enumerate(spread.positions):
                assert pos.meaning, f"{key} position {i+1} missing meaning"
    
    def test_spreads_list_best_uses(self, sample_spreads):
        """DOC-003: Spreads should document when to use them."""
        for key, spread in sample_spreads.items():
            assert len(spread.best_for) >= 3, \
                f"{key} should list at least 3 best uses"
